import re
from typing import List

from numwords_to_nums.tokens_basic import Token, WordType
from numwords_to_nums.rules import FusionRule, LinkingRule
from numwords_to_nums.text_processing_helpers import split_glues, find_similar_word
from numwords_to_nums.constants import OPERATORS


class NumWordsToNum(object):
    def __init__(self, similarity_threshold=1.0, convert_ordinals=True, add_ordinal_ending=False):
        """
        This class can be used to convert text representations of numbers to digits. That is, it replaces all occurrences of numbers (e.g. forty-two) to the digit representation (e.g. 42).

        :param similarity_threshold: Used for spelling correction. It specifies the minimal similarity in the range [0, 1] of a word to one of the number words. 0 inidcates that every other word is similar and 1 requires a perfect match, i.e. no spelling correction is performed with a value of 1.
        :param convert_ordinals: Whether to convert ordinal numbers (e.g. third --> 3).
        :param add_ordinal_ending: Whether to add the ordinal ending to the converted ordinal number (e.g. twentieth --> 20th). Implies convert_ordinals=True.
        """
        self.similarity_threshold = similarity_threshold

        if self.similarity_threshold < 0 or self.similarity_threshold > 1:
            raise ValueError('The similarity_threshold must be in the range [0, 1]')

        self.convert_ordinals = convert_ordinals
        self.add_ordinal_ending = add_ordinal_ending

        # Keeping the ordinal ending implies that we convert ordinal numbers
        if self.add_ordinal_ending:
            self.convert_ordinals = True

    def numerical_words_to_numbers(self, text, convert_operator=False):
        """
        Converts all number representations to digits.

        :param convert_operator: Boolean. Setting this true will also convert the operators in your text
        :param text: The input string.
        :return: The input string with all numbers replaced with their corresponding digit representation. Ordinal numbers will be followed by respective suffix.
        """

        # Tokenize the input string by assigning a type to each word (e.g. representing the number type like units (e.g. one) or teens (twelve))
        # This makes it easier for the subsequent steps to decide which parts of the sentence need to be combined
        # e.g. I like forty-two apples --> I [WordType.Other] like [WordType.Other] forty [WordType.TENS] two [WordType.UNITS] apples [WordType.Other]
        tokens = self._aspect(text)

        # Apply a set of rules to the tokens to combine the numeric tokens and replace them with the corresponding digit
        # e.g. I [WordType.Other] like [WordType.Other] 42 [ConcatenatedToken] apples [WordType.Other] (it merged the TENS and UNITS tokens)

        converted_text = self._portray(tokens).replace('_', '')
        if convert_operator:
            converted_text = self.convert_operators(converted_text)

        return converted_text

    def convert_operators(self, expression_text):
        expression_text = re.sub(' +', ' ', expression_text)
        for operator_word in OPERATORS:
            if operator_word in expression_text:
                # for scenario's like  multiply 3 by 3
                if expression_text.startswith(operator_word) and 'square' not in expression_text:
                    if 'by' in expression_text:
                        expression_text = expression_text.replace(operator_word, '')
                        expression_text = expression_text.replace('by', operator_word)
                    if 'with' in expression_text:
                        expression_text = expression_text.replace(operator_word, '')
                        expression_text = expression_text.replace('with', operator_word)

                valid_pattern = f'\d+ {operator_word} \d+'
                operator_symbol = OPERATORS[operator_word]

                if re.findall('(percent|square)', expression_text):
                    pattern = f' {operator_word}' if 'percent' in expression_text else f'{operator_word} '
                    expression_text = expression_text.replace(pattern, operator_symbol)
                elif re.findall(valid_pattern, expression_text):
                    expression_text = expression_text.replace(f' {operator_word} ', operator_symbol)

        return expression_text

    def _aspect(self, text: str) -> List[Token]:
        """
        This function takes an arbitrary input string, splits it into tokens (words) and assigns each token a type corresponding to the role in the sentence.

        :param text: The input string.
        :return: The tokenized input string.
        """
        tokens = []

        conjunctions = []
        for i, (word, glue) in enumerate(split_glues(text)):
            # Address spelling corrections
            if self.similarity_threshold != 1:
                matched_num = find_similar_word(word, Token.numwords.keys(), self.similarity_threshold)
                if matched_num is not None:
                    word = matched_num
            token = Token(word, glue)
            tokens.append(token)

            # Conjunctions need special treatment since they can be used for both, to combine numbers or to combine other parts in the sentence
            if token.type == WordType.CONJUNCTION:
                conjunctions.append(i)

        # A word should only have the type WordType.CONJUNCTION when it actually combines two digits and not some other words in the sentence
        for i in conjunctions:
            if i >= len(tokens) - 1 or tokens[i + 1].type in [WordType.CONJUNCTION, WordType.OTHER]:
                tokens[i].type = WordType.OTHER

        return tokens

    def _portray(self, tokens: List[Token]) -> str:
        """
        Parses the tokenized input based on predefined rules which combine certain tokens to find the correct digit representation of the textual number description.

        :param tokens: The tokenized input string.
        :return: The transformed input string.
        """
        rules = [FusionRule(), LinkingRule()]

        # Apply each rule to process the tokens
        for rule in rules:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if tokens[i].is_ordinal() and not self.convert_ordinals:
                    # When keeping ordinal numbers, treat the whole number (which may consists of multiple parts, e.g. ninety-seventh) as a normal word
                    tokens[i].type = WordType.OTHER

                if tokens[i].type != WordType.OTHER:

                    # Check how many tokens this rule wants to process...
                    n_match = rule.match(tokens[i:])
                    if n_match > 0:
                        # ... and then merge these tokens into a new one (e.g. a token representing the digit)
                        token = rule.action(tokens[i:i + n_match])
                        new_tokens.append(token)
                        i += n_match
                    else:
                        new_tokens.append(tokens[i])
                        i += 1
                else:
                    new_tokens.append(tokens[i])
                    i += 1

            tokens = new_tokens

        # Combine the tokens back to a string (with special handling of ordinal numbers)
        text = ''
        for token in tokens:
            if token.is_ordinal() and not self.convert_ordinals:
                text += token.word_raw
            else:
                text += token.text()
                if token.is_ordinal() and self.add_ordinal_ending:
                    text += token.ordinal_ending

            text += token.glue

        return text

    @staticmethod
    def evaluate(et):
        # Clean character other than numeric and math characters
        expr_text = ''.join(re.findall("[\d\W]", et))
        # Clean new line, tab and space characters
        expr_text = ''.join(re.findall("[\S]", expr_text))

        result = None
        if re.compile(r'^\d*\s*[\+\-\*\/√%]\s*\d+$').match(expr_text) or re.compile(
                r'^\d*[.]*\d*\s*[\+\-\*\/√%]\s*\d*[.]*\d+$').match(expr_text):
            try:
                result = eval(expr_text)
            except Exception as e:
                result = f" The answer is undefined. Evaluation error: {e}"
        return str(result)


