from elden_ring_wiki.tools.formatters import remove_gallery_content

def test_remove_gallery_content():
    text = """## Section 1

### Section 1.1

### Section 1.2

### Section Gallery
[image1]
[image2]
[image3]

## Section 2

"""
    result = remove_gallery_content(text)
    assert result == """## Section 1

### Section 1.1

### Section 1.2






## Section 2

"""
