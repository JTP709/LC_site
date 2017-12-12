import psycopg2
import datetime
import re
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Blog
from connect import connect

# Add dates to incidents, audits. Rebuild Audit Tables.

# Fake Blog 1
blog_1 = ('1',
          'Generic Title 1',
          'Sub Title 1',
          'Landrover',
          '2017-01-16 15:36:38',
          'general',
          'Lorem ipsum dolor sit amet, ut iriure repudiare sea. Id falli erant qui, saepe instructior no mei. Sed at iusto persius voluptua, eros habeo appetere id cum. At commodo habemus eos, vis ne latine senserit, eam no probo munere consulatu. In nostrum pertinacia vim, ignota necessitatibus sit ea, harum virtute recusabo duo et. Eum veri labore everti ut. Habeo velit cu vim, sit zril audiam singulis an, in legimus accusamus pro.' +
          '<br>At pri solet facilisis. Ei nam invenire intellegat temporibus. Soluta detraxit ius ut, choro veritus mnesarchum est id, viris graece volutpat mea et. An quo senserit persequeris eloquentiam, est agam honestatis no, vis autem postulant philosophia no. Liber latine fabulas ad his, an populo ornatus mandamus ius. Ad nam nobis invidunt vituperatoribus, qui regione accusam philosophia no, accusata volutpat ea nam.' +
          '<br>Ea oblique efficiendi usu. Id quo fastidii definitiones. An voluptua appetere abhorreant vim, quodsi eirmod no qui, quo ut suas nihil graece. Cu scripta prompta delenit mei, fabulas scribentur eum te. No mazim iudicabit voluptatibus his, has quodsi scriptorem ut.'+
          '<br>Id quidam iuvaret vis. Per alterum nominati at, mucius fastidii democritum nam te. Nam ei commodo tibique. Mea ea tantas appareat tacimates, no vix regione nominavi expetendis. Vix et fabellas periculis, ex his habemus nusquam. Accusamus consulatu complectitur eu cum, quas expetenda has ea, mea et error iriure apeirian.'+
          '<br>Ex singulis aliquando mea, nec probo molestiae voluptaria ad. At malorum consequat sea. Rebum iudico no has, vim ut diam atqui quando. Te qui error possit utroque, iudico lobortis et duo, sea eius diceret in.'+
          '<br>An mel errem oratio vulputate, no per vocibus probatus. Causae volutpat mnesarchum sed ex. Qui ut causae mentitum vivendum. Duo dicant deserunt in, ea causae deleniti est, malis detraxit persequeris nec te. Duo alterum incorrupte ea.'+
          '<br>Ad quo oportere hendrerit abhorreant, nec ea putant scriptorem consectetuer. Ne eos duis affert delicata. Exerci melius sed ei, eam te mutat deseruisse. Has eu unum abhorreant, mel feugiat fastidii cu, case possim quo ut.'+
          '<br>Cetero signiferumque ad vim, eam ex vocent ponderum reformidans. Ne legimus efficiendi mei. Ut pro vocibus reformidans, prompta eripuit ne est. Eos ex nonumy intellegat, sea ei vocibus habemus perpetua, id eum ipsum eripuit cotidieque. Eos convenire honestatis ei.'+
          '<br>Mentitum cotidieque cu mel, ad mei sumo iracundia. At tation abhorreant usu, ius in euismod percipit adipisci, quas denique id vix. Doming vivendo argumentum mea an. An epicuri apeirian phaedrum sit.' +
          '<br>Ne vel utinam inermis assentior. Te essent impetus debitis eos, usu solet dissentias id. Melius aliquip voluptatibus sit ne. Enim eius necessitatibus mei id, at case assueverit vel, elit nonumes no vim. In sit dico diceret, est an dolore dolorum facilisis.')

# Fake Blog 1
blog_2 = ('2',
          'Generic Title 2',
          'Sub Title 2',
          'Landrover',
          '2017-01-28 09:10:36',
          'travel',
          'Lorem ipsum dolor sit amet, ut iriure repudiare sea. Id falli erant qui, saepe instructior no mei. Sed at iusto persius voluptua, eros habeo appetere id cum. At commodo habemus eos, vis ne latine senserit, eam no probo munere consulatu. In nostrum pertinacia vim, ignota necessitatibus sit ea, harum virtute recusabo duo et. Eum veri labore everti ut. Habeo velit cu vim, sit zril audiam singulis an, in legimus accusamus pro.' +
          '<br>At pri solet facilisis. Ei nam invenire intellegat temporibus. Soluta detraxit ius ut, choro veritus mnesarchum est id, viris graece volutpat mea et. An quo senserit persequeris eloquentiam, est agam honestatis no, vis autem postulant philosophia no. Liber latine fabulas ad his, an populo ornatus mandamus ius. Ad nam nobis invidunt vituperatoribus, qui regione accusam philosophia no, accusata volutpat ea nam.' +
          '<br>Ea oblique efficiendi usu. Id quo fastidii definitiones. An voluptua appetere abhorreant vim, quodsi eirmod no qui, quo ut suas nihil graece. Cu scripta prompta delenit mei, fabulas scribentur eum te. No mazim iudicabit voluptatibus his, has quodsi scriptorem ut.'+
          '<br>Id quidam iuvaret vis. Per alterum nominati at, mucius fastidii democritum nam te. Nam ei commodo tibique. Mea ea tantas appareat tacimates, no vix regione nominavi expetendis. Vix et fabellas periculis, ex his habemus nusquam. Accusamus consulatu complectitur eu cum, quas expetenda has ea, mea et error iriure apeirian.'+
          '<br>Ex singulis aliquando mea, nec probo molestiae voluptaria ad. At malorum consequat sea. Rebum iudico no has, vim ut diam atqui quando. Te qui error possit utroque, iudico lobortis et duo, sea eius diceret in.'+
          '<br>An mel errem oratio vulputate, no per vocibus probatus. Causae volutpat mnesarchum sed ex. Qui ut causae mentitum vivendum. Duo dicant deserunt in, ea causae deleniti est, malis detraxit persequeris nec te. Duo alterum incorrupte ea.'+
          '<br>Ad quo oportere hendrerit abhorreant, nec ea putant scriptorem consectetuer. Ne eos duis affert delicata. Exerci melius sed ei, eam te mutat deseruisse. Has eu unum abhorreant, mel feugiat fastidii cu, case possim quo ut.'+
          '<br>Cetero signiferumque ad vim, eam ex vocent ponderum reformidans. Ne legimus efficiendi mei. Ut pro vocibus reformidans, prompta eripuit ne est. Eos ex nonumy intellegat, sea ei vocibus habemus perpetua, id eum ipsum eripuit cotidieque. Eos convenire honestatis ei.'+
          '<br>Mentitum cotidieque cu mel, ad mei sumo iracundia. At tation abhorreant usu, ius in euismod percipit adipisci, quas denique id vix. Doming vivendo argumentum mea an. An epicuri apeirian phaedrum sit.' +
          '<br>Ne vel utinam inermis assentior. Te essent impetus debitis eos, usu solet dissentias id. Melius aliquip voluptatibus sit ne. Enim eius necessitatibus mei id, at case assueverit vel, elit nonumes no vim. In sit dico diceret, est an dolore dolorum facilisis.')

# Fake Blog 3
blog_3 = ('3',
          'Generic Title 3',
          'Sub Title 3',
          'Landrover',
          '2017-02-04 21:52:59',
          'crafting',
          'Lorem ipsum dolor sit amet, ut iriure repudiare sea. Id falli erant qui, saepe instructior no mei. Sed at iusto persius voluptua, eros habeo appetere id cum. At commodo habemus eos, vis ne latine senserit, eam no probo munere consulatu. In nostrum pertinacia vim, ignota necessitatibus sit ea, harum virtute recusabo duo et. Eum veri labore everti ut. Habeo velit cu vim, sit zril audiam singulis an, in legimus accusamus pro.' +
          '<br>At pri solet facilisis. Ei nam invenire intellegat temporibus. Soluta detraxit ius ut, choro veritus mnesarchum est id, viris graece volutpat mea et. An quo senserit persequeris eloquentiam, est agam honestatis no, vis autem postulant philosophia no. Liber latine fabulas ad his, an populo ornatus mandamus ius. Ad nam nobis invidunt vituperatoribus, qui regione accusam philosophia no, accusata volutpat ea nam.' +
          '<br>Ea oblique efficiendi usu. Id quo fastidii definitiones. An voluptua appetere abhorreant vim, quodsi eirmod no qui, quo ut suas nihil graece. Cu scripta prompta delenit mei, fabulas scribentur eum te. No mazim iudicabit voluptatibus his, has quodsi scriptorem ut.'+
          '<br>Id quidam iuvaret vis. Per alterum nominati at, mucius fastidii democritum nam te. Nam ei commodo tibique. Mea ea tantas appareat tacimates, no vix regione nominavi expetendis. Vix et fabellas periculis, ex his habemus nusquam. Accusamus consulatu complectitur eu cum, quas expetenda has ea, mea et error iriure apeirian.'+
          '<br>Ex singulis aliquando mea, nec probo molestiae voluptaria ad. At malorum consequat sea. Rebum iudico no has, vim ut diam atqui quando. Te qui error possit utroque, iudico lobortis et duo, sea eius diceret in.'+
          '<br>An mel errem oratio vulputate, no per vocibus probatus. Causae volutpat mnesarchum sed ex. Qui ut causae mentitum vivendum. Duo dicant deserunt in, ea causae deleniti est, malis detraxit persequeris nec te. Duo alterum incorrupte ea.'+
          '<br>Ad quo oportere hendrerit abhorreant, nec ea putant scriptorem consectetuer. Ne eos duis affert delicata. Exerci melius sed ei, eam te mutat deseruisse. Has eu unum abhorreant, mel feugiat fastidii cu, case possim quo ut.'+
          '<br>Cetero signiferumque ad vim, eam ex vocent ponderum reformidans. Ne legimus efficiendi mei. Ut pro vocibus reformidans, prompta eripuit ne est. Eos ex nonumy intellegat, sea ei vocibus habemus perpetua, id eum ipsum eripuit cotidieque. Eos convenire honestatis ei.'+
          '<br>Mentitum cotidieque cu mel, ad mei sumo iracundia. At tation abhorreant usu, ius in euismod percipit adipisci, quas denique id vix. Doming vivendo argumentum mea an. An epicuri apeirian phaedrum sit.' +
          '<br>Ne vel utinam inermis assentior. Te essent impetus debitis eos, usu solet dissentias id. Melius aliquip voluptatibus sit ne. Enim eius necessitatibus mei id, at case assueverit vel, elit nonumes no vim. In sit dico diceret, est an dolore dolorum facilisis.')

# Fake Blog 4
blog_4 = ('4',
          'Generic Title 4',
          'Sub Title 4',
          'Landrover',
          '2017-06-07 01:00:01',
          'baking',
          'Lorem ipsum dolor sit amet, ut iriure repudiare sea. Id falli erant qui, saepe instructior no mei. Sed at iusto persius voluptua, eros habeo appetere id cum. At commodo habemus eos, vis ne latine senserit, eam no probo munere consulatu. In nostrum pertinacia vim, ignota necessitatibus sit ea, harum virtute recusabo duo et. Eum veri labore everti ut. Habeo velit cu vim, sit zril audiam singulis an, in legimus accusamus pro.' +
          '<br>At pri solet facilisis. Ei nam invenire intellegat temporibus. Soluta detraxit ius ut, choro veritus mnesarchum est id, viris graece volutpat mea et. An quo senserit persequeris eloquentiam, est agam honestatis no, vis autem postulant philosophia no. Liber latine fabulas ad his, an populo ornatus mandamus ius. Ad nam nobis invidunt vituperatoribus, qui regione accusam philosophia no, accusata volutpat ea nam.' +
          '<br>Ea oblique efficiendi usu. Id quo fastidii definitiones. An voluptua appetere abhorreant vim, quodsi eirmod no qui, quo ut suas nihil graece. Cu scripta prompta delenit mei, fabulas scribentur eum te. No mazim iudicabit voluptatibus his, has quodsi scriptorem ut.'+
          '<br>Id quidam iuvaret vis. Per alterum nominati at, mucius fastidii democritum nam te. Nam ei commodo tibique. Mea ea tantas appareat tacimates, no vix regione nominavi expetendis. Vix et fabellas periculis, ex his habemus nusquam. Accusamus consulatu complectitur eu cum, quas expetenda has ea, mea et error iriure apeirian.'+
          '<br>Ex singulis aliquando mea, nec probo molestiae voluptaria ad. At malorum consequat sea. Rebum iudico no has, vim ut diam atqui quando. Te qui error possit utroque, iudico lobortis et duo, sea eius diceret in.'+
          '<br>An mel errem oratio vulputate, no per vocibus probatus. Causae volutpat mnesarchum sed ex. Qui ut causae mentitum vivendum. Duo dicant deserunt in, ea causae deleniti est, malis detraxit persequeris nec te. Duo alterum incorrupte ea.'+
          '<br>Ad quo oportere hendrerit abhorreant, nec ea putant scriptorem consectetuer. Ne eos duis affert delicata. Exerci melius sed ei, eam te mutat deseruisse. Has eu unum abhorreant, mel feugiat fastidii cu, case possim quo ut.'+
          '<br>Cetero signiferumque ad vim, eam ex vocent ponderum reformidans. Ne legimus efficiendi mei. Ut pro vocibus reformidans, prompta eripuit ne est. Eos ex nonumy intellegat, sea ei vocibus habemus perpetua, id eum ipsum eripuit cotidieque. Eos convenire honestatis ei.'+
          '<br>Mentitum cotidieque cu mel, ad mei sumo iracundia. At tation abhorreant usu, ius in euismod percipit adipisci, quas denique id vix. Doming vivendo argumentum mea an. An epicuri apeirian phaedrum sit.' +
          '<br>Ne vel utinam inermis assentior. Te essent impetus debitis eos, usu solet dissentias id. Melius aliquip voluptatibus sit ne. Enim eius necessitatibus mei id, at case assueverit vel, elit nonumes no vim. In sit dico diceret, est an dolore dolorum facilisis.')

fake_blogs = (blog_1, blog_2, blog_3, blog_4)

def dueDate(time_stamp):
    date = time_stamp[1]
    dateRegex = re.compile(r'\d\d\d\d-\d\d-\d\d')
    mo = dateRegex.search(date)
    num = mo.group()
    finding_date = datetime.datetime.strptime(num, "%Y-%m-%d")
    week = datetime.timedelta(days=7)
    due_date = finding_date + week
    return due_date

# Connect to the database
con = connect()
Base.metadata.bind = con
print("Connection Created!")
# Creates a session
DBSession = sessionmaker(bind=con)
session = DBSession()
print("Session created!")


def populate():

    for i in range(len(fake_blogs)):
        pop = Blog(bid = fake_blogs[i][0],
                   title = fake_blogs[i][1],
                   sub_title = fake_blogs[i][2],
                   author = fake_blogs[i][3],
                   date_time = fake_blogs[i][4],
                   category = fake_blogs[i][5],
                   content = fake_blogs[i][6],
                   hidden = False)
        session.add(pop)
        session.commit()
        print("Fake Blog #"+str(i)+" added!")

populate()
