"""
Example CLI for piping BOM data to processor for ranking report output
"""
import json
from sys import stdout

from src.line_handlers.line_handler import ReportLimitHandler, Manufacturer, MPN
from src.line_handlers.re_line_handler import RegExBomLineHandler
from src.processor import BomProccessor
from src.record_provider import StdInRecordProvider
from src.reports.running_rank_report import RunningRankingReport


def main():
    report = RunningRankingReport()
    BomProccessor(StdInRecordProvider().records(),
                  [
                      ReportLimitHandler(),
                      RegExBomLineHandler({
                          MPN: 0,
                          Manufacturer: 1
                      }, lambda line: line.count(':') == 2),
                      RegExBomLineHandler({
                          MPN: -2,
                          Manufacturer: -1
                      }, lambda line: line.count(';') == 2),
                      RegExBomLineHandler({
                          MPN: 1,
                          Manufacturer: 0
                      }, lambda line: line.count(' -- ') == 1 and line.count(':') >= 1)
                  ], listeners=[report])

    stdout.write(json.dumps(list(report.run()), indent=4))


if __name__ == '__main__':
    main()
