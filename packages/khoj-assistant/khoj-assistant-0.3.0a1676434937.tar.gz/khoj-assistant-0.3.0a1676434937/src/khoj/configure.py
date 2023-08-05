# Standard Packages
import sys
import logging
import json

# External Packages
import schedule

# Internal Packages
from khoj.processor.ledger.beancount_to_jsonl import BeancountToJsonl
from khoj.processor.markdown.markdown_to_jsonl import MarkdownToJsonl
from khoj.processor.org_mode.org_to_jsonl import OrgToJsonl
from khoj.search_type import image_search, text_search
from khoj.utils.config import SearchType, SearchModels, ProcessorConfigModel, ConversationProcessorConfigModel
from khoj.utils import state
from khoj.utils.helpers import LRU, resolve_absolute_path
from khoj.utils.rawconfig import FullConfig, ProcessorConfig
from khoj.search_filter.date_filter import DateFilter
from khoj.search_filter.word_filter import WordFilter
from khoj.search_filter.file_filter import FileFilter


logger = logging.getLogger(__name__)


def configure_server(args, required=False):
    if args.config is None:
        if required:
            logger.error(f'Exiting as Khoj is not configured.\nConfigure it via GUI or by editing {state.config_file}.')
            sys.exit(1)
        else:
            logger.warn(f'Khoj is not configured.\nConfigure it via khoj GUI, plugins or by editing {state.config_file}.')
            return
    else:
        state.config = args.config

    # Initialize Processor from Config
    state.processor_config = configure_processor(args.config.processor)

    # Initialize the search model from Config
    state.search_index_lock.acquire()
    state.model = configure_search(state.model, state.config, args.regenerate)
    state.search_index_lock.release()


@schedule.repeat(schedule.every(1).hour)
def update_search_index():
    state.search_index_lock.acquire()
    state.model = configure_search(state.model, state.config, regenerate=False)
    state.search_index_lock.release()
    logger.info("Search Index updated via Scheduler")


def configure_search(model: SearchModels, config: FullConfig, regenerate: bool, t: SearchType = None):
    # Initialize Org Notes Search
    if (t == SearchType.Org or t == None) and config.content_type.org:
        # Extract Entries, Generate Notes Embeddings
        model.orgmode_search = text_search.setup(
            OrgToJsonl,
            config.content_type.org,
            search_config=config.search_type.asymmetric,
            regenerate=regenerate,
            filters=[DateFilter(), WordFilter(), FileFilter()])

    # Initialize Org Music Search
    if (t == SearchType.Music or t == None) and config.content_type.music:
        # Extract Entries, Generate Music Embeddings
        model.music_search = text_search.setup(
            OrgToJsonl,
            config.content_type.music,
            search_config=config.search_type.asymmetric,
            regenerate=regenerate,
            filters=[DateFilter(), WordFilter()])

    # Initialize Markdown Search
    if (t == SearchType.Markdown or t == None) and config.content_type.markdown:
        # Extract Entries, Generate Markdown Embeddings
        model.markdown_search = text_search.setup(
            MarkdownToJsonl,
            config.content_type.markdown,
            search_config=config.search_type.asymmetric,
            regenerate=regenerate,
            filters=[DateFilter(), WordFilter(), FileFilter()])

    # Initialize Ledger Search
    if (t == SearchType.Ledger or t == None) and config.content_type.ledger:
        # Extract Entries, Generate Ledger Embeddings
        model.ledger_search = text_search.setup(
            BeancountToJsonl,
            config.content_type.ledger,
            search_config=config.search_type.symmetric,
            regenerate=regenerate,
            filters=[DateFilter(), WordFilter(), FileFilter()])

    # Initialize Image Search
    if (t == SearchType.Image or t == None) and config.content_type.image:
        # Extract Entries, Generate Image Embeddings
        model.image_search = image_search.setup(
            config.content_type.image,
            search_config=config.search_type.image,
            regenerate=regenerate)

    # Invalidate Query Cache
    state.query_cache = LRU()

    return model


def configure_processor(processor_config: ProcessorConfig):
    if not processor_config:
        return

    processor = ProcessorConfigModel()

    # Initialize Conversation Processor
    if processor_config.conversation:
        processor.conversation = configure_conversation_processor(processor_config.conversation)

    return processor


def configure_conversation_processor(conversation_processor_config):
    conversation_processor = ConversationProcessorConfigModel(conversation_processor_config)
    conversation_logfile = resolve_absolute_path(conversation_processor.conversation_logfile)

    if conversation_logfile.is_file():
        # Load Metadata Logs from Conversation Logfile
        with conversation_logfile.open('r') as f:
            conversation_processor.meta_log = json.load(f)
        logger.info('Conversation logs loaded from disk.')
    else:
        # Initialize Conversation Logs
        conversation_processor.meta_log = {}
        conversation_processor.chat_session = ""

    return conversation_processor
