import unittest

from dataclasses import dataclass
from typing import List

from iamsystem.brat.adapter import BratDocument
from iamsystem.brat.adapter import BratEntity
from iamsystem.brat.adapter import BratNote
from iamsystem.brat.adapter import BratWriter
from iamsystem.brat.formatter import IndividualTokenFormatter
from iamsystem.brat.formatter import SpanFormatter
from iamsystem.brat.formatter import TokenStopFormatter
from iamsystem.brat.util import get_brat_format
from iamsystem.brat.util import get_brat_format_seq
from iamsystem.keywords.keywords import Keyword
from iamsystem.matcher.matcher import Matcher
from iamsystem.tokenization.api import IToken
from iamsystem.tokenization.token import Offsets
from iamsystem.tokenization.tokenize import french_tokenizer


class BratUtilsTest(unittest.TestCase):
    """Brat utility functions."""

    def setUp(self) -> None:
        self.tokenizer = french_tokenizer()
        self.tokens: List[IToken] = list(
            self.tokenizer.tokenize("meningo-encéphalite")
        )

    def test_get_brat_format(self):
        """Brat offsets format of meningo token."""
        span_id = get_brat_format(self.tokens[0])
        self.assertEqual("0 7", span_id)

    def test_get_brat_format_seq(self):
        """Brat offsets format of the two tokens."""
        span_id = get_brat_format_seq(self.tokens)
        self.assertEqual("0 7;8 19", span_id)


class BratEntityTest(unittest.TestCase):
    """Brat entity connector."""

    def setUp(self) -> None:
        self.entity_id = "T1"
        self.offsets = get_brat_format_seq([Offsets(0, 4)])
        self.offsets_discontinuous = get_brat_format_seq(
            [Offsets(0, 4), Offsets(8, 12)]
        )
        self.text = "hello"
        self.brat_type = "Person"

    def test_to_string(self):
        """Entity string representation."""
        brat_entity = BratEntity(
            entity_id=self.entity_id,
            brat_type=self.brat_type,
            offsets=self.offsets,
            text=self.text,
        )
        self.assertEqual("T1	Person 0 4	hello", str(brat_entity))

    def test_to_string_discontinuous_words(self):
        """Entity string representation when tokens are discontinuous."""
        brat_entity = BratEntity(
            entity_id=self.entity_id,
            brat_type=self.brat_type,
            offsets=self.offsets_discontinuous,
            text=self.text,
        )
        self.assertEqual("T1	Person 0 4;8 12	hello", str(brat_entity))

    def test_bad_entity_id(self):
        """Entity id must start by the letter T."""
        with self.assertRaises(ValueError):
            BratEntity(
                entity_id="1",
                brat_type=self.brat_type,
                offsets=self.offsets,
                text=self.text,
            )

    def test_to_brat_format(self):
        matcher = Matcher.build(
            keywords=["cancer prostate"], stopwords=["de", "la"], w=2
        )
        annots = matcher.annot_text(text="cancer de la prostate")
        self.assertEqual(annots[0].to_brat_format(), "0 6;13 21")
        self.assertEqual(
            str(annots[0]), "cancer prostate	0 6;13 21	cancer prostate"
        )

    def test_to_brat_format_leading_stop(self):
        matcher = Matcher.build(
            keywords=["cancer prostate"], stopwords=["de", "la"], w=2
        )
        annots = matcher.annot_text(text="cancer de la glande prostate")
        self.assertEqual(annots[0].to_brat_format(), "0 6;20 28")
        self.assertEqual(
            str(annots[0]), "cancer prostate	0 6;20 28	cancer prostate"
        )  # noqa


class BraNoteTest(unittest.TestCase):
    """Brat notes connector."""

    def setUp(self) -> None:
        self.note_id = "#1"
        self.ref_id = "T1"
        self.note = "leucodermie (C3714505)"
        self.text = "Le mot leucodermie"

    def test_to_string(self):
        """Brat note string representation."""
        brat_note = BratNote(
            note_id=self.note_id, ref_id=self.ref_id, note=self.note
        )
        self.assertEqual(
            "#1\tIAMSYSTEM T1\tleucodermie (C3714505)", str(brat_note)
        )

    def test_bad_note_id(self):
        """a Brat note id must start by '#'."""
        with self.assertRaises(ValueError):
            BratNote(note_id="1", ref_id=self.ref_id, note=self.note)


@dataclass
class MyEntity(Keyword):
    """A keyword that stores a brat_type to pass it to the connector."""

    brat_type: str

    def __str__(self):
        return f"{self.label} ({self.brat_type})"


class BratDocumentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.entity_id = "T1"
        self.offsets = get_brat_format_seq([Offsets(0, 4)])
        self.text = "hello"
        self.brat_type = "Person"

        matcher = Matcher()
        ent1 = MyEntity(label="North America", brat_type="NA")
        ent2 = MyEntity(label="South America", brat_type="SA")
        matcher.add_keywords(keywords=[ent1, ent2])
        matcher.w = 3
        self.text_america = "North and South America"
        self.annots = matcher.annot_text(text=self.text_america)

    def test_add_entity(self):
        """Add a Brat entity works."""
        brat_document = BratDocument()
        brat_document.add_entity(
            brat_type=self.brat_type, offsets=self.offsets, text=self.text
        )
        self.assertEqual(1, len(brat_document.brat_entities))

    def test_to_string_empty(self):
        """If no entities added, return an empty string."""
        brat_document = BratDocument()
        self.assertEqual("", str(brat_document))

    def test_to_string_entities(self):
        """Brat entities string representation when multiples
        entities are added."""
        brat_document = BratDocument()
        brat_document.add_entity(
            brat_type=self.brat_type, offsets=self.offsets, text=self.text
        )
        brat_document.add_entity(
            brat_type=self.brat_type, offsets=self.offsets, text=self.text
        )
        self.assertEqual(
            "T1\tPerson 0 4\thello\nT2\tPerson 0 4\thello",
            brat_document.entities_to_string(),
        )

    def test_to_string_brat_document(self):
        """Brat document contains entities and notes string representation."""
        matcher = Matcher()
        ent1 = MyEntity(label="North America", brat_type="NA")
        matcher.add_keywords(keywords=[ent1])
        matcher.w = 3
        annots = matcher.annot_text(text=self.text_america)
        brat_document = BratDocument()
        brat_document.add_annots(annots, brat_type="COUNTRY")

        self.assertEqual(
            "T1\tCOUNTRY 0 5;16 23\tNorth America\n#1\tIAMSYSTEM T1\tNorth "
            "America (NA)",
            str(brat_document),
        )

    def test_add_annots_value_error(self):
        """keyword_attr or brat_type must be set. Raise if both None."""
        brat_document = BratDocument()
        with self.assertRaises(ValueError):
            brat_document.add_annots(self.annots)

    def test_add_annots_brat_type(self):
        """The brat_type parameter value is in the string representation."""
        brat_document = BratDocument()
        brat_document.add_annots(self.annots, brat_type="COUNTRY")
        self.assertEqual(
            "T1\tCOUNTRY 0 5;16 23\tNorth America\nT2\tCOUNTRY 10 23\tSouth "
            "America",
            brat_document.entities_to_string(),
        )

    def test_add_annots_keyattr(self):
        """The brat_type attribute of the Entity class
        is in the string representation."""
        matcher = Matcher()
        entity1 = MyEntity(label="France", brat_type="COUNTRY")
        entity2 = MyEntity(label="South America", brat_type="CONTINENT")
        matcher.add_keywords(keywords=[entity1, entity2])
        annots = matcher.annot_text(text="France and South America")
        brat_document = BratDocument()
        brat_document.add_annots(annots, keyword_attr="brat_type")
        self.assertEqual(
            "T1\tCOUNTRY 0 6\tFrance\nT2\tCONTINENT 11 24\tSouth America",
            brat_document.entities_to_string(),
        )

    def test_brat_writer(self):
        """check save functions raise no error."""
        brat_document = BratDocument()
        brat_document.add_annots(self.annots, brat_type="COUNTRY")
        # filename = "./test.ann"
        # with(open(filename, 'w')) as p:
        # BratWriter.saveEntities(brat_entities=brat_document, write=p.write)
        BratWriter.saveEntities(
            brat_entities=brat_document.get_entities(), write=lambda x: None
        )
        BratWriter.saveNotes(
            brat_notes=brat_document.get_notes(), write=lambda x: None
        )

    def test_similar_stopwords_window_strategy(self):
        """Test stopwords and window strategies give the same output."""
        matcher = Matcher.build(
            keywords=["cancer prostate"], stopwords=["de", "la"], w=1
        )
        annots_stop = matcher.annot_text(text="cancer de la prostate")
        matcher = Matcher.build(keywords=["cancer prostate"], w=3)
        annots_w = matcher.annot_text(text="cancer de la prostate")
        self.assertEqual(annots_stop[0].to_string(), annots_w[0].to_string())


class BratFormatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.matcher = Matcher.build(
            keywords=["cancer prostate"], stopwords=["de", "la"], w=2
        )
        self.text = "cancer de la glande prostate"
        annots = self.matcher.annot_text(text=self.text)
        self.annot = annots[0]

    def test_default(self):
        """Default is to group continuous sequence of tokens."""
        self.assertEqual(
            self.annot.to_string(), "cancer prostate	0 6;20 28	cancer prostate"
        )

    def test_stop_true(self):
        """BratTokenAndStop remove trailing sequence of stopwords.
        Here 'de', 'la' that are trailing thus removed."""
        self.annot.brat_formatter = TokenStopFormatter()  # default True
        self.assertEqual(
            self.annot.to_string(), "cancer prostate	0 6;20 28	cancer prostate"
        )

    def test_stop_true_2(self):
        """BratTokenAndStop remove trailing sequence of stopwords.
        Here 'de', 'la' that are not trailing thus not removed."""
        annots = self.matcher.annot_text(text="cancer de la prostate")
        annot = annots[0]
        annot.brat_formatter = TokenStopFormatter()  # default True
        self.assertEqual(
            annot.to_string(), "cancer de la prostate	0 21	cancer prostate"
        )

    def test_stop_false(self):
        """Keep stopwords inside annotation, 'de', 'la' are present."""
        self.annot.brat_formatter = TokenStopFormatter(False)
        self.assertEqual(
            self.annot.to_string(),
            "cancer de la prostate	0 12;20 28	cancer prostate",
        )

    def test_span(self):
        """Simply take start and end offsets of the annotation."""
        self.annot.brat_formatter = SpanFormatter(text=self.text)
        self.assertEqual(
            self.annot.to_string(),
            "cancer de la glande prostate	0 28	cancer prostate",
        )

    def test_individual(self):
        """Check it outputs offsets for each token."""
        annots = self.matcher.annot_text(text="cancer prostate")
        annot = annots[0]
        annot.brat_formatter = IndividualTokenFormatter()
        self.assertEqual(
            annot.to_string(), "cancer prostate	0 6;7 15	cancer prostate"
        )


if __name__ == "__main__":
    unittest.main()
