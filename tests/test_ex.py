from ga import GA
import ga.ex as ex

def test_sortbydist():
	ga = GA(3)

	p1 = [ga.e3 * 1.0]
	p2 = [ga.e3 * 2.0]

	rs = ex.sortbydist(ga, B = ga.e12, q = ga.vector())(
		[p1, p2]
	)

	assert rs == [p2, p1], str(rs)


