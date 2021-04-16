"""
OWASP Maryam!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import concurrent.futures

meta = {
	'name': 'Iris Meta Search Engine(experiment version)',
	'author': 'Aman',
	'version': '0.1',
	'description': 'Iris is a built-in meta search engine.',
	'contributors': 'Saeed, Dimitris, Divya, Vikas, Kunal',
	'sources': ('google', 'yahoo', 'bing', 'etools', 'metacrawler', 'searx', 'dogpile'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 10, False, 'Number of results per page(default=10)', '-c', 'store', int),
	),
	'examples': ('iris -q <QUERY> -l 15 --output --api',)
}
RESULTS = []
COUNT_CONSENSUS = None
LIMIT_CONSENSUS = None
def thread(self, function, engines, query):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=len(engines))
	futures = (threadpool.submit(function, self, engine, query) for engine in engines)
	counter = 1
	for _ in concurrent.futures.as_completed(futures):
		pass

def search(self, name, q):
	global RESULTS
	engine = getattr(self, name)
	limit = LIMIT_CONSENSUS[name] or 1
	count = COUNT_CONSENSUS[name]
	if count:
		if name == 'google':
			attr = engine(q, limit, count, 'legacy')
		else:
			attr = engine(q, limit, count)

		attr.run_crawl()
		if name == 'google':
			RESULTS.append(attr.results_legacy)
		else:
			RESULTS.append(attr.results)

def module_api(self):
	global COUNT_CONSENSUS, LIMIT_CONSENSUS
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = ['google', 'yahoo']
	engines_len = len(engines)
	COUNT_CONSENSUS = self.meta_search_util.compute_count_consensus(engines, count)
	LIMIT_CONSENSUS = self.meta_search_util.compute_count_consensus(engines, limit)
	thread(self, search, engines, query)
	simple_merge = []
	for i in range(len(min(RESULTS, key=len))):
		for e in range(len(engines)):
			simple_merge.append(RESULTS[e%engines_len][i])
	output = {'results': simple_merge}
	self.save_gather(output, 'iris/iris', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
