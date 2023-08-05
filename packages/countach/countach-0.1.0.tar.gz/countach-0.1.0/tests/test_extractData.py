# The expected output data
import testdata.output as data
import src.countach as countach

def test_extractData():
	output = countach.extractData("tests/testdata/newvcu_2.a2l")
	assert output == data.output
