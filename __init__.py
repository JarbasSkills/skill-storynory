from os.path import join, dirname

from audiobooker.scrappers.storynory import StoryNory
from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.parse import fuzzy_match, MatchStrategy
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search


class StoryNorySkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super(StoryNorySkill, self).__init__("StoryNory")
        self.supported_media = [MediaType.GENERIC, MediaType.AUDIOBOOK]
        self.skill_icon = join(dirname(__file__), "ui", "logo.png")

    def calc_score(self, phrase, match, idx=0, base_score=0):
        # idx represents the order from search
        score = base_score - idx  # - 1% as we go down the results list

        score += 100 * fuzzy_match(phrase.lower(), match.title.lower(),
                                   strategy=MatchStrategy.TOKEN_SET_RATIO)

        return min(100, score)

    # common play
    @ocp_search()
    def search_audiobooks(self, phrase, media_type):
        # match the request media_type
        base_score = 0
        if media_type == MediaType.AUDIOBOOK:
            base_score += 25
        else:
            base_score -= 15

        if self.voc_match(phrase, "storynory"):
            # explicitly requested storynory
            base_score += 60
            phrase = self.remove_voc(phrase, "storynory")

        loyalbooks = StoryNory()

        results = loyalbooks.search_audiobooks(title=phrase)
        for book in self._yield_results(phrase, results, base_score):
            yield book

    def _yield_results(self, phrase, results, base_score=0):
        for idx, book in enumerate(results):
            score = self.calc_score(phrase, book, idx=idx,
                                    base_score=base_score)
            yield self._book2ocp(book, score)

    def _book2ocp(self, book, score):
        author = " ".join([au.first_name + au.last_name for au in
                            book.authors])
        pl = [{
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "uri": s,
            "artist": author,
            "playback": PlaybackType.AUDIO,
            "image": book.img,
            "bg_image": book.img,
            "skill_icon": self.skill_icon,
            "title": str(book.title) + f" (part {ch + 1})",
            "skill_id": self.skill_id
        } for ch, s in enumerate(book.streams)]

        return {
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "playback": PlaybackType.AUDIO,
            "playlist": pl,  # return full playlist result
            "length": book.runtime * 1000,
            "image": book.img,
            "artist": author,
            "bg_image": book.img,
            "skill_icon": self.skill_icon,
            "title": book.title,
            "skill_id": self.skill_id
        }


def create_skill():
    return StoryNorySkill()
