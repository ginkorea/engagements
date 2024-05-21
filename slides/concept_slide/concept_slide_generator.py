from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN
from data.server import data_server


class ContentBox:
    def __init__(self, engagement):
        self.engagement = engagement

    def add_to_slide(self, slide):
        raise NotImplementedError("Subclasses should implement this method")


class FiveWBox(ContentBox):
    def add_to_slide(self, slide):
        left = Inches(0.5)
        top = Inches(0.5)
        width = Inches(4)
        height = Inches(4.5)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame

        p = text_frame.add_paragraph()
        p.text = f"Event: {self.engagement['engagement']}"
        p.space_after = Inches(0.1)
        p.font.bold = True

        p = text_frame.add_paragraph()
        p.text = f"Date/Time: {self.engagement['date']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Location: {self.engagement['location']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Line of Effort: {self.engagement['loe']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Subordinate Objective: {self.engagement['subordinate_objective']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Purpose: {self.engagement['purpose']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"2ID/RUCD Attendees: {self.engagement['2id_rucd_attendees']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Relevant Attendees: {self.engagement['relevant_attendees']}"
        p.space_after = Inches(0.1)

        p = text_frame.add_paragraph()
        p.text = f"Uniform: {self.engagement['uniform']}"
        p.space_after = Inches(0.1)


class ConceptSlide:
    def __init__(self, presentation, engagement):
        self.engagement = engagement
        self.prs = presentation
        self.slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])

    def add_boxes(self):
        five_w_box = FiveWBox(self.engagement)
        five_w_box.add_to_slide(self.slide)


class ConceptSlideGenerator:
    def __init__(self):
        self.engagements = data_server.sample_engagements
        self.presentation = Presentation()

    def generate_slides(self, output_file):
        for _, engagement in self.engagements.iterrows():
            slide = ConceptSlide(self.presentation, engagement)
            slide.add_boxes()
            print('added boxes to slide for %s' % engagement['engagement'])

        self.presentation.save(output_file)


# Example usage
generator = ConceptSlideGenerator()
generator.generate_slides('concept_slides.pptx')
