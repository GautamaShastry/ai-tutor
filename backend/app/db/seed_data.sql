-- Seed data for Telugu AI Tutor

-- Skill Concepts for Telugu Language Learning
-- Categories: tense, marker, case, pronunciation, script

-- Script Reading Concepts (Foundation)
INSERT INTO skill_concepts (id, name, category, description, prerequisites) VALUES
('a1000000-0000-0000-0000-000000000001', 'Telugu Vowels (అచ్చులు)', 'script', 'Learn the 16 Telugu vowels: అ, ఆ, ఇ, ఈ, ఉ, ఊ, ఋ, ౠ, ఎ, ఏ, ఐ, ఒ, ఓ, ఔ, అం, అః', '{}'),
('a1000000-0000-0000-0000-000000000002', 'Telugu Consonants (హల్లులు)', 'script', 'Learn the 36 Telugu consonants organized by articulation point', '{}'),
('a1000000-0000-0000-0000-000000000003', 'Vowel Signs (మాత్రలు)', 'script', 'Learn how vowels combine with consonants to form syllables', '{a1000000-0000-0000-0000-000000000001,a1000000-0000-0000-0000-000000000002}'),
('a1000000-0000-0000-0000-000000000004', 'Conjunct Consonants (సంయుక్తాక్షరాలు)', 'script', 'Learn consonant clusters and how they are written', '{a1000000-0000-0000-0000-000000000002,a1000000-0000-0000-0000-000000000003}'),
('a1000000-0000-0000-0000-000000000005', 'Telugu Numerals', 'script', 'Learn Telugu number system: ౦, ౧, ౨, ౩, ౪, ౫, ౬, ౭, ౮, ౯', '{}');

-- Pronunciation Concepts
INSERT INTO skill_concepts (id, name, category, description, prerequisites) VALUES
('b1000000-0000-0000-0000-000000000001', 'Retroflex Sounds (ట, ఠ, డ, ఢ, ణ)', 'pronunciation', 'Master the retroflex consonants unique to Telugu', '{a1000000-0000-0000-0000-000000000002}'),
('b1000000-0000-0000-0000-000000000002', 'Aspirated Consonants', 'pronunciation', 'Distinguish between aspirated and unaspirated sounds', '{a1000000-0000-0000-0000-000000000002}'),
('b1000000-0000-0000-0000-000000000003', 'ళ vs ల Distinction', 'pronunciation', 'Master the difference between ళ (retroflex lateral) and ల (dental lateral)', '{b1000000-0000-0000-0000-000000000001}'),
('b1000000-0000-0000-0000-000000000004', 'Vowel Length', 'pronunciation', 'Distinguish between short and long vowels in speech', '{a1000000-0000-0000-0000-000000000001}'),
('b1000000-0000-0000-0000-000000000005', 'Sandhi Rules', 'pronunciation', 'Learn phonological rules for combining sounds at word boundaries', '{b1000000-0000-0000-0000-000000000001,b1000000-0000-0000-0000-000000000004}');

-- Tense Concepts
INSERT INTO skill_concepts (id, name, category, description, prerequisites) VALUES
('c1000000-0000-0000-0000-000000000001', 'Present Tense (వర్తమానకాలం)', 'tense', 'Form and use present tense verbs: -తున్నాను, -తున్నావు, etc.', '{a1000000-0000-0000-0000-000000000003}'),
('c1000000-0000-0000-0000-000000000002', 'Past Tense (భూతకాలం)', 'tense', 'Form and use past tense verbs: -ను, -వు, -డు, etc.', '{c1000000-0000-0000-0000-000000000001}'),
('c1000000-0000-0000-0000-000000000003', 'Future Tense (భవిష్యత్కాలం)', 'tense', 'Form and use future tense verbs: -తాను, -తావు, etc.', '{c1000000-0000-0000-0000-000000000001}'),
('c1000000-0000-0000-0000-000000000004', 'Habitual Aspect', 'tense', 'Express habitual actions and routines', '{c1000000-0000-0000-0000-000000000001}'),
('c1000000-0000-0000-0000-000000000005', 'Perfect Aspect', 'tense', 'Express completed actions with present relevance', '{c1000000-0000-0000-0000-000000000002}');

-- Case Marker Concepts
INSERT INTO skill_concepts (id, name, category, description, prerequisites) VALUES
('d1000000-0000-0000-0000-000000000001', 'Nominative Case', 'case', 'Subject marking in Telugu sentences', '{a1000000-0000-0000-0000-000000000003}'),
('d1000000-0000-0000-0000-000000000002', 'Accusative Case (-ని/-ను)', 'case', 'Direct object marking', '{d1000000-0000-0000-0000-000000000001}'),
('d1000000-0000-0000-0000-000000000003', 'Dative Case (-కి/-కు)', 'case', 'Indirect object and purpose marking', '{d1000000-0000-0000-0000-000000000001}'),
('d1000000-0000-0000-0000-000000000004', 'Genitive Case (-యొక్క)', 'case', 'Possession and relationship marking', '{d1000000-0000-0000-0000-000000000001}'),
('d1000000-0000-0000-0000-000000000005', 'Locative Case (-లో/-మీద)', 'case', 'Location and position marking', '{d1000000-0000-0000-0000-000000000003}'),
('d1000000-0000-0000-0000-000000000006', 'Instrumental Case (-తో)', 'case', 'Means and accompaniment marking', '{d1000000-0000-0000-0000-000000000003}');

-- Grammatical Marker Concepts
INSERT INTO skill_concepts (id, name, category, description, prerequisites) VALUES
('e1000000-0000-0000-0000-000000000001', 'Plural Markers (-లు)', 'marker', 'Form plural nouns in Telugu', '{a1000000-0000-0000-0000-000000000003}'),
('e1000000-0000-0000-0000-000000000002', 'Postpositions', 'marker', 'Use Telugu postpositions: మీద, కింద, ముందు, వెనుక, etc.', '{d1000000-0000-0000-0000-000000000005}'),
('e1000000-0000-0000-0000-000000000003', 'Question Markers', 'marker', 'Form questions using -ఆ, ఏమి, ఎవరు, ఎక్కడ, etc.', '{c1000000-0000-0000-0000-000000000001}'),
('e1000000-0000-0000-0000-000000000004', 'Negation (-లేదు, కాదు)', 'marker', 'Express negation in different tenses', '{c1000000-0000-0000-0000-000000000001,c1000000-0000-0000-0000-000000000002}'),
('e1000000-0000-0000-0000-000000000005', 'Honorific Markers', 'marker', 'Use appropriate honorific forms: -గారు, -వారు', '{e1000000-0000-0000-0000-000000000001}'),
('e1000000-0000-0000-0000-000000000006', 'Verb Agreement', 'marker', 'Match verb endings with subject person, number, and gender', '{c1000000-0000-0000-0000-000000000001,e1000000-0000-0000-0000-000000000001}');

-- Sample Achievements
INSERT INTO achievements (id, name, description, icon, xp_reward, criteria) VALUES
('f1000000-0000-0000-0000-000000000001', 'First Steps', 'Complete your first lesson', 'star', 10, '{"type": "lessons_completed", "value": 1}'),
('f1000000-0000-0000-0000-000000000002', 'Week Warrior', 'Maintain a 7-day streak', 'fire', 50, '{"type": "streak", "value": 7}'),
('f1000000-0000-0000-0000-000000000003', 'Vocabulary Builder', 'Learn 50 new words', 'book', 30, '{"type": "vocabulary_count", "value": 50}'),
('f1000000-0000-0000-0000-000000000004', 'Script Master', 'Master all script concepts', 'scroll', 100, '{"type": "category_mastered", "value": "script"}'),
('f1000000-0000-0000-0000-000000000005', 'Conversation Starter', 'Complete 10 chat sessions', 'chat', 40, '{"type": "chat_sessions", "value": 10}');
