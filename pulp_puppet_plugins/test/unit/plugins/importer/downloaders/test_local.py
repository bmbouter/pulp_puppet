import os

import mock

import base_downloader
from pulp_puppet.common import constants, model
from pulp_puppet.plugins.importers.downloaders.exceptions import FileRetrievalException
from pulp_puppet.plugins.importers.downloaders.local import LocalDownloader


DATA_DIR = os.path.abspath(os.path.dirname(__file__)) + '/../../../../data'
VALID_REPO_DIR = os.path.join(DATA_DIR, 'repos', 'valid')
INVALID_REPO_DIR = os.path.join(DATA_DIR, 'repos', 'invalid')


class LocalDownloaderTests(base_downloader.BaseDownloaderTests):

    def setUp(self):
        super(LocalDownloaderTests, self).setUp()
        self.config.repo_plugin_config[constants.CONFIG_FEED] = 'file://' + VALID_REPO_DIR
        self.downloader = LocalDownloader(self.repo, None, self.config)

    @mock.patch('nectar.config.DownloaderConfig.finalize')
    def test_retrieve_metadata(self, mock_finalize):
        # Test
        docs = self.downloader.retrieve_metadata(self.mock_progress_report)

        # Verify
        self.assertEqual(1, len(docs))
        metadata = model.RepositoryMetadata()
        metadata.update_from_json(docs[0])
        self.assertEqual(2, len(metadata.modules))

        self.assertEqual(1, self.mock_progress_report.metadata_query_total_count)
        self.assertEqual(1, self.mock_progress_report.metadata_query_finished_count)
        expected_query = os.path.join(VALID_REPO_DIR, constants.REPO_METADATA_FILENAME)
        self.assertEqual(expected_query, self.mock_progress_report.metadata_current_query)
        self.assertEqual(2, self.mock_progress_report.update_progress.call_count)

        mock_finalize.assert_called_once()

    def test_retrieve_metadata_no_metadata_found(self):
        # Setup
        self.config.repo_plugin_config[constants.CONFIG_FEED] = 'file://' + INVALID_REPO_DIR

        # Test
        try:
            self.downloader.retrieve_metadata(self.mock_progress_report)
            self.fail()
        except FileRetrievalException:
            pass

    def test_retrieve_module(self):
        # Test
        mod_path = self.downloader.retrieve_module(self.mock_progress_report, self.module)

        # Verify
        expected = os.path.join(VALID_REPO_DIR, self.module.filename())
        self.assertEqual(expected, mod_path)

    def test_retrieve_module_no_file(self):
        # Setup
        self.module.author = 'foo'

        # Test
        try:
            self.downloader.retrieve_module(self.mock_progress_report, self.module)
            self.fail()
        except FileRetrievalException:
            pass

    def test_cleanup_module(self):
        # Test
        self.downloader.cleanup_module(self.module)

        # This test makes sure the default NotImplementedError is not raised
