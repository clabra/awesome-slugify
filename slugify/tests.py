# coding=utf8

import unittest

from slugify import Slugify, UniqueSlugify
from slugify import slugify, slugify_unicode, unique_slugify
from slugify import slugify_url, slugify_filename
from slugify import slugify_ru, slugify_de, slugify_el

from slugify import get_slugify


class SlugifyTestCase(unittest.TestCase):

    def test_slugify_english(self):
        self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
        self.assertEqual(slugify('_this_is_a__test___'), 'this-is-a-test')
        self.assertEqual(slugify('- - -This -- is a ## test ---'), 'This-is-a-test')

    def test_slugify_umlaut(self):
        self.assertEqual(slugify('kožušček'), 'kozuscek',)
        self.assertEqual(slugify('C\'est déjà l\'été.'), 'Cest-deja-lete')
        self.assertEqual(slugify('jaja---lol-méméméoo--a'), 'jaja-lol-mememeoo-a')
        self.assertEqual(slugify('Nín hǎo. Wǒ shì zhōng guó rén'), 'Nin-hao-Wo-shi-zhong-guo-ren')
        self.assertEqual(slugify('Programmes de publicité - Solutions d\'entreprise'),
                         'Programmes-de-publicite-Solutions-dentreprise')

    def test_slugify_chinese(self):
        self.assertEqual(slugify('北亰'), 'Bei-Jing')

    def test_slugify_russian(self):
        self.assertEqual(slugify('Компьютер'), 'Kompiuter')
        self.assertEqual(slugify('Транслитерирует и русский'), 'Transliteriruet-i-russkii')
        self.assertEqual(slugify('ёжик из щуки сварил уху'), 'iozhik-iz-shchuki-svaril-ukhu')
        self.assertEqual(slugify('Ах, Юля-Юля'), 'Akh-Iulia-Iulia')

    def test_slugify_ru(self):
        self.assertEqual(slugify_ru('Компьютер'), 'Komputer')
        self.assertEqual(slugify_ru('Транслитерирует и русский'), 'Transliteriryet-i-rysskii')
        self.assertEqual(slugify_ru('ёжик из щуки сварил уху'), 'ezhik-iz-schyki-svaril-yhy')
        self.assertEqual(slugify_ru('Ах, Юля-Юля'), 'Ah-Ulya-Ulya')

    def test_slugify_de(self):
        self.assertEqual(slugify_de('Öl und SÜD'), 'Oel-und-SUED')

    def test_greek(self):
        self.assertEqual(slugify_el('ϒ Ϋ υ ϋ ΰ'), 'Y-Y-y-y-y')

    def test_slugify_unicode(self):
        self.assertEqual(slugify_unicode('-=Слово по-русски=-'), u'Слово-по-русски')
        self.assertEqual(slugify_unicode('слово_по_русски'), u'слово-по-русски')


class PredefinedSlugifyTestCase(unittest.TestCase):

    def test_slugify_url(self):
        self.assertEqual(slugify_url('The Über article'), 'the-uber-article')

    def test_slugify_filename(self):
        self.assertEqual(slugify_filename(u'Дrаft №2.txt'), u'Draft_2.txt')


class ToLowerTestCase(unittest.TestCase):

    def test_to_lower(self):
        self.assertEqual(slugify('Test TO lower', to_lower=True), 'test-to-lower')

    def test_to_lower_arg(self):
        slugify = Slugify()
        slugify.to_lower = True

        self.assertEqual(slugify('Test TO lower'), 'test-to-lower')
        self.assertEqual(slugify('Test TO lower', to_lower=False), 'Test-TO-lower')

    def test_to_lower_with_capitalize(self):
        self.assertEqual(slugify('Test TO lower', to_lower=True, capitalize=True), 'Test-to-lower')

    def test_to_lower_with_unicode(self):
        self.assertEqual(slugify('自転車', to_lower=True), 'zi-zhuan-che')


class UpperTestCase(unittest.TestCase):
    def test_full_upper(self):
        self.assertEqual(slugify_ru('ЯНДЕКС'), 'YANDEKS')

    def test_camel_word(self):
        self.assertEqual(slugify_ru('Яндекс'), 'Yandeks')
        self.assertEqual(slugify_ru('UP Яндекс'), 'UP-Yandeks')
        self.assertEqual(slugify_ru('Яндекс UP'), 'Yandeks-UP')

    def test_part_of_word(self):
        self.assertEqual(slugify_de('ÜBERslugify'), 'UEBERslugify')
        self.assertEqual(slugify_de('ÜBERslugifÜ AUF'), 'UEBERslugifUE-AUF')

    def test_at_start_of_sentence(self):
        self.assertEqual(slugify_ru('Я пошёл'), 'Ya-poshel')
        self.assertEqual(slugify_ru('Я Пошёл'), 'Ya-Poshel')
        self.assertEqual(slugify_ru('Я ПОШёл'), 'YA-POSHel')
        self.assertEqual(slugify_ru('Я ПОШЁЛ. Я Пошел'), 'YA-POSHEL-Ya-Poshel')

    def test_at_end_of_sentence(self):
        self.assertEqual(slugify_ru('пошЁЛ Я'), 'poshEL-YA')
        self.assertEqual(slugify_ru('пошЁЛ Я.'), 'poshEL-YA')
        self.assertEqual(slugify_ru('пошёл Я. ПОШЁЛ'), 'poshel-Ya-POSHEL')

    def test_one_letter_words(self):
        self.assertEqual(slugify_ru('Э Я Г Д Е ?'), 'E-Ya-G-D-E')
        self.assertEqual(slugify_ru('UP Э Я Г Д Е ?'), 'UP-E-YA-G-D-E')

    def test_abbreviation(self):
        self.assertEqual(slugify_ru('UP Я.Б.Ч'), 'UP-Ya-B-Ch')


class PretranslateTestCase(unittest.TestCase):

    def test_pretranslate(self):
        EMOJI_TRANSLATION = {
            u'ʘ‿ʘ': u'smiling',
            u'ಠ_ಠ': u'disapproval',
            u'♥‿♥': u'enamored',
            u'♥': u'love',

            u'(c)': u'copyright',
            u'©': u'copyright',
        }
        slugify_emoji = Slugify(pretranslate=EMOJI_TRANSLATION)
        self.assertEqual(slugify_emoji(u'ʘ‿ʘ'), u'smiling')
        self.assertEqual(slugify_emoji(u'ಠ_ಠ'), u'disapproval')
        self.assertEqual(slugify_emoji(u'(c)'), u'copyright')
        self.assertEqual(slugify_emoji(u'©'), u'copyright')

    def test_pretranslate_lambda(self):
        slugify_reverse = Slugify(pretranslate=lambda value: value[::-1])
        self.assertEqual(slugify_reverse('slug'), 'guls')

    def test_wrong_argument_type(self):
        self.assertRaises(ValueError, lambda: Slugify(pretranslate={1, 2}))


class SanitizeTestCase(unittest.TestCase):
    def test_sanitize(self):
        self.assertEqual(slugify('test_sanitize'), 'test-sanitize')

    def test_safe_chars(self):
        slugify = Slugify()

        slugify.safe_chars = '_'
        self.assertEqual(slugify('test_sanitize'), 'test_sanitize')

        slugify.safe_chars = "'"
        self.assertEqual(slugify('Конь-Огонь'), "Kon'-Ogon'")


class StopWordsTestCase(unittest.TestCase):
    def test_stop_words(self):
        slugify = Slugify(stop_words=['a', 'the'])

        self.assertEqual(slugify('A red apple'), 'red-apple')
        self.assertEqual(slugify('The4 red apple'), 'The4-red-apple')

        self.assertEqual(slugify('_The_red_the-apple'), 'red-apple')
        self.assertEqual(slugify('The__red_apple'), 'red-apple')

        slugify.safe_chars = '*'
        self.assertEqual(slugify('*The*red*apple'), '*-*red*apple')
        self.assertEqual(slugify('The**red*apple'), '**red*apple')

        slugify.stop_words = ['x', 'y']
        self.assertEqual(slugify('x y n'), 'n')


class TruncateTestCase(unittest.TestCase):

    def test_truncate(self):
        self.assertEqual(slugify('one two three four', max_length=7), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=8), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=12), 'one-two-four')
        self.assertEqual(slugify('one two three four', max_length=13), 'one-two-three')
        self.assertEqual(slugify('one two three four', max_length=14), 'one-two-three')

    def test_truncate_on_empty(self):
        self.assertEqual(slugify('', max_length=10), '')

    def test_truncate_short(self):
        self.assertEqual(slugify('dlinnoeslovo', max_length=7), 'dlinnoe')
        self.assertEqual(slugify('dlinnoeslovo и ещё слово', max_length=11), 'dlinnoeslov')

    def test_truncate_long(self):
        self.assertEqual(slugify('шшш щщщ слово', max_length=11), 'shshsh')
        self.assertEqual(slugify('шшш щщщ слово', max_length=12), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=18), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=19), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=24), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=25), 'shshsh-shchshchshch-slovo')

    def test_truncate_unwanted(self):
        self.assertEqual(slugify('...one...two...three...four...', max_length=12), 'one-two-four')

    def test_truncate_long_separator(self):
        self.assertEqual(slugify('one two three four', max_length=14, separator='...'), 'one...two')


class OtherTestCase(unittest.TestCase):

    def test_prevent_double_pretranslation(self):
        slugify = Slugify(pretranslate={'s': 'ss'})
        self.assertEqual(slugify('BOOST'), 'BOOSST')

    def test_capitalize(self):
        self.assertEqual(slugify('this Is A test', capitalize=True), 'This-Is-A-test')

    def test_capitalize_on_empty(self):
        self.assertEqual(slugify('', capitalize=True), '')


class UniqueTestCase(unittest.TestCase):

    def test_unique_slugify(self):
        self.assertEqual(unique_slugify('This % is a test ---'), 'This-is-a-test')
        self.assertEqual(unique_slugify('- - -This -- is a ## test ---'), 'This-is-a-test-1')
        self.assertEqual(unique_slugify('_this_is_a__test___'), 'this-is-a-test')

    def test_unique(self):
        slugify = UniqueSlugify()
        self.assertEqual(slugify('This % is another test ---'), 'This-is-another-test')
        self.assertEqual(slugify('- - -This -- is another ## test ---'), 'This-is-another-test-1')

    def test_init_uids(self):
        slugify = UniqueSlugify(uids=['This-is-my-test', 'This-is-another-test'])
        self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
        self.assertEqual(slugify('This % is my test ---'), 'This-is-my-test-1')

    def test_init_other(self):
        slugify = UniqueSlugify(separator=u'_')
        self.assertEqual(slugify('This % is another test ---'), 'This_is_another_test')
        self.assertEqual(slugify('- - -This -- is another ## test ---'), 'This_is_another_test_1')

    def test_unique_other(self):
        slugify = UniqueSlugify()
        self.assertEqual(slugify('This % is another test ---', separator='_'), 'This_is_another_test')
        self.assertEqual(slugify('- - -This -- is another ## test ---', separator='_'), 'This_is_another_test_1')


class DeprecationTestCase(unittest.TestCase):

    def test_deprecated_get_slugify(self):
        import warnings

        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter('once')

            slugify = get_slugify()
            self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
            self.assertIn("'slugify.get_slugify' is deprecated", str(warning[-1].message))


class PhraseSlugifyTestCase(unittest.TestCase):

    def test_slugify_phrase_url(self):
        text = "Someone must have slandered Josef K., for one morning, without having done anything truly wrong, he was arrested."
        self.assertEqual(slugify_url(text),
                "someone-must-have-slandered-josef-k")

        text = "The Miss Lonelyhearts of the New York Post-Dispatch (Are you in trouble?—Do-you-need-advice?—Write-to-Miss-Lonelyhearts-and-she-will-help-you) sat at his desk and stared at a piece of white cardboard. —Nathanael West, Miss Lonelyhearts"
        self.assertEqual(slugify_url(text),
                "the-miss-lonelyhearts-of-the-new-york-post-dispatch-are-you-in-trouble-do-you-need-advice-write")

        text = " I wish either my father or my mother, or indeed both of them, as they were in duty both equally bound to it, had minded what they were about when they begot me; had they duly considered how much depended upon what they were then doing;—that not only the production of a rational Being was concerned in it, but that possibly the happy formation and temperature of his body, perhaps his genius and the very cast of his mind;—and, for aught they knew to the contrary, even the fortunes of his whole house might take their turn from the humours and dispositions which were then uppermost:—Had they duly weighed and considered all this, and proceeded accordingly,—I am verily persuaded I should have made a quite different figure in the world, from that, in which the reader is likely to see me. —Laurence Sterne, Tristram Shandy (1759–1767)"
        self.assertEqual(slugify_url(text),
                "i-wish-either-my-father-or-my-mother-or-indeed-both-of-them")


if __name__ == '__main__':
    unittest.main()
