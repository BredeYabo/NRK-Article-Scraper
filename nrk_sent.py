from polyglot.text import Text

text = Text(
    "En person er sendt til sykehus etter at et bolighus brant i Bangsund. To nabohus ble evakuert på grunn av spredningsfare. Brannvesenet kom til brannstedet litt før klokka 07. Da var bolighuset overtent.  På grunn av spredningsfare, ble det etter kort tid besluttet å sette i verk evakuering av to nabohus. Beboerne har nå flyttet inn igjen. Det forteller operasjonsleder i politiet Ole Petter Hollingen til NRK. Operasjonsleder hos politiet, Ole Petter Hollingen, forteller like etter klokka 08 til NRK at én person er sendt til sykehus for nærmere sjekk, etter å ha pustet inn røyk fra brannen. Mannen bor i huset som brant. Brannvesenet melder at de har kontroll på brannen, men boligen er totalskadd. Brannfolk jobber med slukking i Bangsund. Richard Lindseth bor i nabolaget. Han fortalte til NRK klokka 7.30 at det fremdeles brenner, men at ilden ikke har spredt seg til nabobygninger.  – Jeg oppdaget at det brant gjennom vinduet i huset mitt rett borti her. Da jeg kom ut så jeg flammer slå opp fra taket på nabohuset, det var nok overtent allerede, forteller Richard Lindseth.")
print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))

# print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
# for w in text.words:
# print("{:<16}{:>2}".format(w, w.polarity))

first_sentence = text
print(first_sentence)
first_entity = first_sentence.entities[0]
print(first_entity)

for word in text.entities:
    print(str(word) + ": Positiv : " + str(word.positive_sentiment))
    print(str(word) + ": Negativ : " + str(word.negative_sentiment))
