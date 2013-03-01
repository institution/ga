import ga.mv as mv

def test__gen_grade_masks():
	rr = mv._gen_grade_slices(3)
	er = [(0,1), (1,4), (4,7), (7,8)]
		
	assert rr == er, (repr(rr), repr(er))
	

