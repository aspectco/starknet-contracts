# Build and test
build :; nile compile
test  :; pytest tests/

test-erc721 :; pytest tests/test_erc721.py -s -v
test-shortstring :; pytest tests/test_shortstring.py -s -v

