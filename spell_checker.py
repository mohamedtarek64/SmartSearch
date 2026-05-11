import difflib

class SpellChecker:
    def __init__(self, index_terms):
        """Initializes dictionary from existing search index terms."""
        self.dictionary = list(index_terms.keys())

    def suggest(self, query):
        """Provides spelling suggestions based on string similarity."""
        if not query: return None
        
        words = query.lower().split()
        suggestions = []
        is_corrected = False

        for word in words:
            # Find the closest match in the dictionary with 80% similarity threshold
            matches = difflib.get_close_matches(word, self.dictionary, n=1, cutoff=0.8)
            
            if matches and matches[0] != word:
                suggestions.append(matches[0])
                is_corrected = True
            else:
                suggestions.append(word)
        
        return " ".join(suggestions) if is_corrected else None
