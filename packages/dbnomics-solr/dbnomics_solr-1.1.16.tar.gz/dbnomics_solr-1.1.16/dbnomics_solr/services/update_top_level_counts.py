"""Domain-level service to update the counts of providers, datasets and series."""

import daiquiri

from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["update_top_level_counts"]


logger = daiquiri.getLogger(__name__)


def update_top_level_counts(*, commit: bool = True, dbnomics_solr_client: DBnomicsSolrClient):
    """Update the counts of providers, datasets and series."""

    logger.debug("Querying the top-level counts...")
    counts = dbnomics_solr_client.get_counts(force_count=True)

    logger.debug("Indexing the top-level counts: %r", counts)
    dbnomics_solr_client.index_counts(counts)

    if commit:
        dbnomics_solr_client.commit()

    logger.info("Top-level counts were updated: %r", counts)
