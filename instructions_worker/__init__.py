from otree.api import *
import pandas as pd
import random
import time

df1 = pd.read_excel('_static\global\worker_pairs_decision.xlsx', keep_default_na=False, engine='openpyxl')

"""
Fragen: 
- Wie kann man die Profile wieder "freigeben", wenn Leute aufhören? 
- Profilabfrage: Was passiert, wenn falsch?  
- für employer stage 2: score sequences task (erste 10/ random 10 Fragen/ +/- random number / group level information...)

ToDo:
- Literatur zu Motivation/ performance/ competition (statistical discrimination)
- hide Timer evtl. außer letzte 30 sek anzeigen & checken ob es funktioniert (dass Seite dann nicht mehr angezeigt wird)
- evtl. auch timer auf instructions part 2/ silder... ausweiten (?)
- excel-liste employer "verdoppeln" (pro worker nicht pro pair) und entsprechend auslesen
- emplyer1: alle Variablen, die in otree stehen sollen speichern (checken) --> diese Liste dann einlesen quasi für worker
- Scores für sequences task evtl. direkt in excel schreiben (Kopie von excel), wenn es geht (dass mehrere parallel drauf zugreifen) 
- hiring Frage erst nach sequences task (worker wissen vorher nicht, dass task sich nochmal auf hiring auswirkt)
- overview: baseline experiment + possible extensions 
- random treatment: allen vorher sagen, dass ein paar von PC überschrieben werden und dann auf treatment Seite sagen, 
    dass Person "betroffen" ist (unten dann) 
- bonus für erste Runde hiring --> auch einbauen in Übersicht am Ende
- Profilabfrage falsch (oder kein freies Profil) [kein freies profil: evtl. auch random eins nehmen] --> anderes Experiment 
- question einbauen, worauf die workers die Entscheidung zurückführen (Insb. ob Diskriminierung)
- dropout-timeout: was dann anzeigen? 
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions_worker'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    session = 6  # set session number according to the profile for which the session is created (1: male, white, 20-24 / 2: male, white, 25-29 / ... 5: male, black, 20-24)
                    # (only thing that needs to be changed but also om treatment info page!)
    gender = ['male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'female',
              'female', 'female', 'female', 'female', ]
    race = ['White', 'White', 'White', 'White', 'Black or African American', 'Black or African American',
            'Black or African American',
            'Black or African American', 'White', 'White', 'White', 'White', 'Black or African American',
            'Black or African American',
            'Black or African American', 'Black or African American', ]
    # to check if correct profile
    age_lb = [20, 25, 30, 35, 20, 25, 30, 35, 20, 25, 30, 35, 20, 25, 30, 35, ]
    age_ub = [24, 29, 34, 39, 24, 29, 34, 39, 24, 29, 34, 39, 24, 29, 34, 39, ]
    # Version 2
    """
    # jeweils a-x nach Anzahl an Workern pro Profil reinschreiben
    labels_alle_sessions = [['1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', ],
                            ['2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', ],
                            ['3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', ],
                            ['4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', ],
                            ['5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', ],
                            ['6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b', ],
                            ['7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', ],
                            ['8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', ],
                            ['9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', ],
                            ['10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', ],
                            ['11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', ],
                            ['12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b'],
                            ['13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', ],
                            ['14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', ],
                            ['15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', ],
                            ['16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', ],
                            ]
    """


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    session.used_labels = []


""" version 1 - works, but drop-out-problem
def creating_session(subsession):
    labels_session_1 = ['1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b' ]
    random.shuffle(labels_session_1)
    labels_session_2 = ['2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b' ]
    random.shuffle(labels_session_2)
    labels_session_3 = ['3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b' ]
    random.shuffle(labels_session_3)
    labels_session_4 = ['4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b' ]
    random.shuffle(labels_session_4)
    labels_session_5 = ['5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b' ]
    random.shuffle(labels_session_5)
    labels_session_6 = ['6a','6b', '6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b' ]
    random.shuffle(labels_session_6)
    labels_session_7 = ['7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b' ]
    random.shuffle(labels_session_7)
    labels_session_8 = ['8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b' ]
    random.shuffle(labels_session_8)
    labels_session_9 = ['9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b' ]
    random.shuffle(labels_session_9)
    labels_session_10 = ['10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b' ]
    random.shuffle(labels_session_10)
    labels_session_11 = ['11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b' ]
    random.shuffle(labels_session_11)
    labels_session_12 = ['12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b' ]
    random.shuffle(labels_session_12)
    labels_session_13 = ['13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b' ]
    random.shuffle(labels_session_13)
    labels_session_14 = ['14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b' ]
    random.shuffle(labels_session_14)
    labels_session_15 = ['15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b' ]
    random.shuffle(labels_session_15)
    labels_session_16 = ['16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b' ]
    random.shuffle(labels_session_16)
    i = C.session
    for player in subsession.get_players():
        player.participant.label = labels_alle_sessions[i-1][player.id_in_group - 1]
        """


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Abfrage hat bisher noch keine Auswirkungen, außer dass dann wrong_profile = True ist
    gender = models.StringField(
        choices=['male', 'female', 'other', 'prefer not to say'],
        label='<b>What is your gender?</b>',
        widget=widgets.RadioSelect,
    )
    race = models.StringField(
        choices=["Hispanic or Latin", "Asian", "White", "Black or African American",
                 "other / prefer not to answer"],
        label='<b>What is your race?</b>',
        widgets=widgets.RadioSelect,
    )
    age = models.IntegerField(label="")
    consent = models.BooleanField()
    prolificid = models.CharField(initial=None,
                                  verbose_name="Before we start, please provide your Prolific ID.")
    wrong_profile = models.BooleanField(initial=False)


# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']


class ID(Page):
    form_model = 'player'
    form_fields = ['prolificid', 'gender', 'race', 'age', ]

    """ Version 1 
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        k = C.session - 1
        if player.gender != C.gender[k] or player.race != C.race[k] or player.age <= C.age_lb[k] or player.age >= \
                C.age_ub[k]:
            print('Wrong profile')
            player.wrong_profile = True
            participant.wrong_profile = player.wrong_profile
        i = C.session
        i = df1[df1['IDWorker'] == player.participant.label].index[0]
        print(i)
        participant.decision_pair = {'worker_id': df1['IDWorker'][i],
                                     'gender': df1['gender'][i],
                                     'race': df1['race'][i],
                                     'agegroup': df1["agegroup"][i],
                                     'opponent_id': df1["IDOpponent"][i],
                                     'gender_opp': df1["genderOpp"][i],
                                     'race_opp': df1["raceOpp"][i],
                                     'agegroup_opp': df1["agegroupOpp"][i],
                                     'decisions_pro': df1["decisionspro"][i],
                                     'decisions_con': df1["decisionscon"][i],
                                     'treatment': df1["treatment"][i],
                                     }
        print("DECISION PAIR", participant.decision_pair)
        """

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        player.wrong_profile = False
        participant.wrong_profile = player.wrong_profile
        k = C.session - 1
        if player.gender != C.gender[k] or player.race != C.race[k] or player.age <= C.age_lb[k] or player.age >= \
                C.age_ub[k]:
            print('Wrong profile')
            player.wrong_profile = True
            participant.wrong_profile = player.wrong_profile
        session = player.session
        """
        moved to app after first sequences task 
        # noch keine gute Lösung wegen drop outs:
        if not player.wrong_profile:
            if C.labels_alle_sessions[k][player.id_in_group - 1] not in session.used_labels:
                player.participant.label = C.labels_alle_sessions[k][player.id_in_group - 1]
                # evtl. change to corresponding session-profile-list to use random labels
                session.used_labels.append(player.participant.label)
                # add option to take other profile-label if that is not used yet
            else: # sollte am besten nicht passieren
                player.participant.label = "1b"
            # change to something else... None?
            print ("list of used labels", session.used_labels)
        else:
            player.participant.label = "1a" #change for experiment to None or something (experiment ends)
        i = df1[df1['IDWorker'] == player.participant.label].index[0] # gives row number of corresponding label in excel
        print(i)
        participant.decision_pair = {'worker_id': df1['IDWorker'][i],
                                     'gender': df1['gender'][i],
                                     'race': df1['race'][i],
                                     'agegroup': df1["agegroup"][i],
                                     'opponent_id': df1["IDOpponent"][i],
                                     'gender_opp': df1["genderOpp"][i],
                                     'race_opp': df1["raceOpp"][i],
                                     'agegroup_opp': df1["agegroupOpp"][i],
                                     'decisions_pro': df1["decisionspro"][i],
                                     'decisions_con': df1["decisionscon"][i],
                                     'treatment': df1["treatment"][i],
                                     }
        print("DECISION PAIR", participant.decision_pair)
        # evtl. move to end of sequences_before (would eliminate problem of dropouts before that task)
        """


class Alt(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.wrong_profile


class Instructions(Page):
    pass
    """
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        session = player.session
        elapsed_time = time.time() - participant.start_time
        if elapsed_time > C.max_time_start:
            participant.time_exceeded = True
            print("TIME EXCEEDED")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                print ("updated list", session.used_labels)
            else:
                print ("label not in list")
    """


page_sequence = [Consent, ID, Alt, Instructions]
