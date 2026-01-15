from . import remove_empty_sections, append_h4_to_subheaders, remove_gallery_content, remove_multiple_empty_lines, remove_video_guide
class FormatBuilder:
    def __init__(self, text: str):
        self.text = text
    
    def remove_empty_sections(self):
        self.text = remove_empty_sections(self.text)
        return self
    
    def append_h4_to_subheaders(self):
        self.text = append_h4_to_subheaders(self.text)
        return self
    
    def remove_gallery_content(self):
        self.text = remove_gallery_content(self.text)
        return self
    
    def remove_multiple_empty_lines(self):
        self.text = remove_multiple_empty_lines(self.text)
        return self
    
    def remove_video_guide(self):
        self.text = remove_video_guide(self.text)
        return self 
    
    def build(self):
        return self.text