import types
from unittest.mock import MagicMock

from game.processor import IngestionPipeline


def make_stage(return_value):
    stage = MagicMock()
    stage.process.side_effect = (
        return_value if callable(return_value) else lambda row: return_value
    )
    return stage


class TestIngestionPipeline:
    def test_yields_row_through_single_stage(self):
        rows = [{"id": "1", "name": "levy"}]
        stage = make_stage(lambda row: row)
        pipeline = IngestionPipeline(rows=rows, stages=[stage])

        result = list(pipeline.process())

        assert result == [{"id": "1", "name": "levy"}]

    def test_yields_row_through_multiple_stages(self):
        rows = [{"id": "1", "name": "levy"}]
        stage1 = make_stage(lambda row: {**row, "tag": "A"})
        stage2 = make_stage(lambda row: {**row, "extra": "yes"})
        pipeline = IngestionPipeline(rows=rows, stages=[stage1, stage2])

        result = list(pipeline.process())

        assert result == [
            {
                "id": "1",
                "name": "levy",
                "tag": "A",
                "extra": "yes",
            },
        ]

    def test_drops_row_when_stage_returns_none(self):
        rows = [{"id": "1"}, {"id": "2"}]
        stage = make_stage(lambda row: None if row["id"] == "1" else row)
        pipeline = IngestionPipeline(rows=rows, stages=[stage])

        result = list(pipeline.process())

        assert result == [{"id": "2"}]

    def test_drops_all_rows_when_all_filtered(self):
        rows = [{"id": "1"}, {"id": "2"}]
        stage = make_stage(None)
        pipeline = IngestionPipeline(rows=rows, stages=[stage])

        result = list(pipeline.process())

        assert result == []

    def test_stops_processing_stages_after_none(self):
        rows = [{"id": "1"}]
        stage1 = make_stage(None)
        stage2 = make_stage(lambda row: row)
        pipeline = IngestionPipeline(rows=rows, stages=[stage1, stage2])

        list(pipeline.process())

        stage1.process.assert_called_once()
        stage2.process.assert_not_called()

    def test_no_stages_yields_rows_unchanged(self):
        rows = [{"id": "1"}, {"id": "2"}]
        pipeline = IngestionPipeline(rows=rows, stages=[])

        result = list(pipeline.process())

        assert result == [{"id": "1"}, {"id": "2"}]

    def test_empty_rows_yields_nothing(self):
        stage = make_stage(lambda row: row)
        pipeline = IngestionPipeline(rows=[], stages=[stage])

        result = list(pipeline.process())

        assert result == []

    def test_process_is_lazy_generator(self):
        rows = [{"id": "1"}]
        pipeline = IngestionPipeline(rows=rows, stages=[])

        assert isinstance(pipeline.process(), types.GeneratorType)

    def test_each_stage_receives_output_of_previous(self):
        rows = [{"id": "1"}]
        stage1 = make_stage(lambda row: {"id": "modified"})
        stage2 = MagicMock()
        stage2.process.side_effect = lambda row: row
        pipeline = IngestionPipeline(rows=rows, stages=[stage1, stage2])

        list(pipeline.process())

        stage2.process.assert_called_once_with({"id": "modified"})

    def test_multiple_rows_processed_independently(self):
        rows = [{"id": "1"}, {"id": "?"}, {"id": "3"}]
        stage = make_stage(lambda row: None if row["id"] == "?" else row)
        pipeline = IngestionPipeline(rows=rows, stages=[stage])

        result = list(pipeline.process())

        assert result == [{"id": "1"}, {"id": "3"}]
