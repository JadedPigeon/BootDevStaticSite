class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTMLNode to_html()")
    
    def props_to_html(self):
        props_string = ""
        if self.props != None:
            for key in self.props:
                props_string += f' {key}="{self.props[key]}"'
        return props_string
            
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.children = None

    def to_html(self):
        if self.value == None:
            raise ValueError("no value for LeafNode to_html()")
        if self.tag == None:
            return self.value
        props_html = self.props_to_html()
        html = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        return html
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if not children:
            raise ValueError("ParentNode must have at least one child")
        if not tag:
            raise ValueError("ParentNode requires a valid tag")
        self.value = None

    def to_html(self):
        html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{html}</{self.tag}>"

    