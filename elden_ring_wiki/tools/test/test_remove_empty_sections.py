from elden_ring_wiki.tools.formatters import remove_empty_sections


def test_remove_empty_sections():
    text = """
## Section 1  
hello
## Section 2  
hello2

## Section 3  
hello3
### Section 3.1  
  
### Section 3.2  
  
## Section 4

## Section 5
Hello5
"""
    result = remove_empty_sections(text)
    assert (
        result
        == 
"""
## Section 1  
hello
## Section 2  
hello2

## Section 3  
hello3






## Section 5
Hello5
"""
    )
