from percolation.rdf import NS, po, a, c
from percolation.rdf.publishing import TranslationPublishing
import percolation as P, numpy as n, nltk as k, os, re, datetime, shutil
from participation import PACKAGEDIR


class AAPublishing(TranslationPublishing):
    hastext=True
    isinteraction=False
    isfriendship=False
    isego=False
    isgroup=False
    def __init__(self,snapshotid,final_path="some_snapshots/",umbrella_dir=None):
        TranslationPublishing.__init__(self,final_path,umbrella_dir,snapshotid)
        final_path_="{}{}/".format(final_path,self.snapshotid)
        if not umbrella_dir:
            umbrella_dir=final_path
        online_prefix="https://raw.githubusercontent.com/OpenLinkedSocialData/{}master/{}/".format(umbrella_dir,self.snapshotid)
        if not os.path.isdir(final_path):
            os.mkdir(final_path)
        if not os.path.isdir(final_path_):
            os.mkdir(final_path_)
        size_chars_overall=[]; size_tokens_overall=[]; size_sentences_overall=[]
        locals_=locals().copy(); del locals_["self"]
        for i in locals_:
            exec("self.{}={}".format(i,i))
    def makeMetadata(self):
        return
        qtriples=[
                 ("?fooshout",po.shoutText,"?text"),
                 ]
        self.totalchars=sum(                self.size_chars_overall)
        self.mchars_messages=n.mean(        self.size_chars_overall)
        self.dchars_messages=n.std(         self.size_chars_overall)
        self.totaltokens=sum(              self.size_tokens_overall)
        self.mtokens_messages=n.mean(      self.size_tokens_overall)
        self.dtokens_messages=n.std(       self.size_tokens_overall)
        self.totalsentences=sum(        self.size_sentences_overall)
        self.msentences_messages=n.mean(self.size_sentences_overall)
        self.dsentences_messages=n.std( self.size_sentences_overall)
        self.nmessages=P.get("SELECT (COUNT(?s) as ?s) WHERE { ?s a po:Shout }",context=self.translation_graph)
        self.nparticipants=P.get("SELECT (COUNT(?s) as ?s) WHERE { ?s a po:Participant }",context=self.translation_graph)
        self.nurls=P.get("SELECT (COUNT(?s) as ?s) WHERE { ?s po:hasUrl ?o }",context=self.translation_graph)
        triples=[
                (self.snapshoturi, po.nParticipants,     self.nparticipants),
                (self.snapshoturi, po.nMessages,         self.nmessages),
                (self.snapshoturi, po.nCharsOverall,     self.totalchars),
                (self.snapshoturi, po.mCharsOverall,     self.mchars_messages),
                (self.snapshoturi, po.dCharsOverall,     self.dchars_messages),
                (self.snapshoturi, po.nTokensOverall,    self.totaltokens),
                (self.snapshoturi, po.mTokensOverall,    self.mtokens_messages),
                (self.snapshoturi, po.dTokensOverall,    self.dtokens_messages),
                (self.snapshoturi, po.nSentencesOverall, self.totalsentences),
                (self.snapshoturi, po.mSentencesOverall, self.msentences_messages),
                (self.snapshoturi, po.dSentencesOverall, self.dsentences_messages),
                ]
        P.add(triples,context=self.meta_graph)
        P.rdf.triplesScaffolding(self.snapshoturi,
                [po.ParticipantAttribute]*len(self.participantvars),
                self.participantvars,context=self.meta_graph)
        P.rdf.triplesScaffolding(self.snapshoturi,
                [po.MessageAttribute]*len(self.messagevars),
                self.messagevars,context=self.meta_graph)
        P.rdf.triplesScaffolding(self.snapshoturi,
                [po.shoutXMLFilename]*len(self.translation_xml)+[po.shoutTTLFilename]*len(self.translation_ttl),
                self.translation_xml+self.translation_ttl,context=self.meta_graph)
        P.rdf.triplesScaffolding(self.snapshoturi,
                [po.onlineShoutXMLFile]*len(self.translation_xml)+[po.onlineShoutTTLFile]*len(self.translation_ttl),
                [self.online_prefix+i for i in self.translation_xml+self.translation_ttl],context=self.meta_graph)

        self.mrdf=self.snapshotid+"Meta.rdf"
        self.mttl=self.snapshotid+"Meta.ttl"
        self.desc="irc dataset with snapshotID: {}\nsnapshotURI: {} \nisEgo: {}. isGroup: {}.".format(
                                                self.snapshotid,self.snapshoturi,self.isego,self.isgroup,)
        self.desc+="\nisFriendship: {}; ".format(self.isfriendship)
        self.desc+="isInteraction: {}.".format(self.isinteraction)
        self.nchecks=P.get(r"SELECT (COUNT(?checker) as ?cs) WHERE { ?foosession po:checkParticipant ?checker}",context=self.translation_graph)
        self.desc+="\nnParticipants: {}; nInteractions: {} (only session checks in first aa).".format(self.nparticipants,self.nchecks)
        self.desc+="\nisPost: {} (alias hasText: {})".format(self.hastext,self.hastext)
        self.desc+="\nnMessages: {}; ".format(self.nmessages)

        self.desc+="\nnCharsOverall: {}; mCharsOverall: {}; dCharsOverall: {}.".format(self.totalchars,                    self.mchars_messages,     self.dchars_messages)
        self.desc+="\nnTokensOverall: {}; mTokensOverall: {}; dTokensOverall: {};".format(self.totaltokens,               self.mtokens_messages,    self.dtokens_messages)
        self.desc+="\nnSentencesOverall: {}; mSentencesOverall: {}; dSentencesOverall: {};".format(self.totalsentences,self.msentences_messages, self.dsentences_messages)
        self.desc+="\nnURLs: {}; nAAMessages {}.".format(self.nurls,self.nmessages)
        triples=[
                (self.snapshoturi, po.triplifiedIn,      datetime.datetime.now()),
                (self.snapshoturi, po.triplifiedBy,      "scripts/"),
                (self.snapshoturi, po.donatedBy,         self.snapshotid[:-4]),
                (self.snapshoturi, po.availableAt,       self.online_prefix),
                (self.snapshoturi, po.onlineMetaXMLFile, self.online_prefix+self.mrdf),
                (self.snapshoturi, po.onlineMetaTTLFile, self.online_prefix+self.mttl),
                (self.snapshoturi, po.metaXMLFileName,   self.mrdf),
                (self.snapshoturi, po.metaTTLFileName,   self.mttl),
                (self.snapshoturi, po.totalXMLFileSizeMB, self.size_xml),
                (self.snapshoturi, po.totalTTLFileSizeMB, self.size_ttl),
                (self.snapshoturi, po.acquiredThrough,   "aa shouts in "+self.snapshotid),
                (self.snapshoturi, po.socialProtocolTag, "AA"),
                (self.snapshoturi, po.socialProtocol,    P.rdf.ic(po.Platform,"IRC",self.meta_graph,self.snapshoturi)),
                (self.snapshoturi, po.nTriples,         self.ntranslation_triples),
                (self.snapshoturi, NS.rdfs.comment,         self.desc),
                ]
        P.add(triples,self.meta_graph)

    def writeAll(self):
        g=P.context(self.meta_graph)
        ntriples=len(g)
        triples=[
                 (self.snapshoturi,po.nMetaTriples,ntriples)      ,
                 ]
        P.add(triples,context=self.meta_graph)
        g.namespace_manager.bind("po",po)
        g.serialize(self.final_path_+self.snapshotid+"Meta.ttl","turtle"); c("ttl")
        g.serialize(self.final_path_+self.snapshotid+"Meta.rdf","xml")
        c("serialized meta")
        if not os.path.isdir(self.final_path_+"scripts"):
            os.mkdir(self.final_path_+"scripts")
        shutil.copy(PACKAGEDIR+"/../tests/triplify.py",self.final_path_+"scripts/triplify.py")
        # copia do base data
        text="""structure in the RDF/XML file(s):
{}
and the Turtle file(s):
{}
(anonymized: False "nicks inteface").""".format( self.nparticipants,str(self.participantvars),
                    self.nchecks,self.ndirect,self.nmention,
                    self.translation_xml,
                    self.translation_ttl)
        tposts="""\n\nThe dataset consists of {} shout messages with metadata {}
{:.3f} characters in average (std: {:.3f}) and total chars in snapshot: {}
{:.3f} tokens in average (std: {:.3f}) and total tokens in snapshot: {}
{:.3f} sentences in average (std: {:.3f}) and total sentences in snapshot: {}""".format(
                        self.nmessages,str(self.messagevars),
                        self.mcharsmessages, self.dcharsmessages,self.totalchars,
                        self.mtokensmessages,self.dtokensmessages,self.totaltokens,
                        self.msentencesmessages,self.dsentencesmessages,self.totalsentences,
                        )
        self.dates=P.get(r"SELECT ?date WHERE { GRAPH <%s> { ?fooshout po:createdAt ?date } "%(self.translation_graph,))
        self.dates=[i.isoformat() for i in self.dates]
        date1=min(self.dates)
        date2=max(self.dates)
        with open(self.final_path_+"README","w") as f:
            f.write("""::: Open Linked Social Data publication
\nThis repository is a RDF data expression of the IRC
snapshot {snapid} with tweets from {date1} to {date2}
(total of {ntrip} triples).{tinteraction}{tposts}
\nMetadata for discovery in the RDF/XML file:
{mrdf} \nor in the Turtle file:\n{mttl}
\nEgo network: {ise}
Group network: {isg}
Friendship network: {isf}
Interaction network: {isi}
Has text/posts: {ist}
\nAll files should be available at the git repository:
{ava}
\n{desc}

The script that rendered this data publication is on the script/ directory.\n:::""".format(
                snapid=self.snapshotid,date1=date1,date2=date2,ntrip=self.ntriples,
                        tinteraction=tposts,
                        tposts=tposts,
                        mrdf=self.translation_xml,
                        mttl=self.translation_ttl,
                        ise=self.isego,
                        isg=self.isgroup,
                        isf=self.isfriendship,
                        isi=self.isinteraction,
                        ist=self.hastext,
                        ava=self.online_prefix,
                        desc=self.desc
                        ))

    regex_url=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    def addText(self,messageuri,messagetext):
        size_chars=len(messagetext)
        size_tokens=len(k.wordpunct_tokenize(messagetext))
        size_sentences=len(k.sent_tokenize(  messagetext))
        triples=[
                (messageuri, po.textMessage, messagetext),
                (messageuri, po.nChars,       size_chars),
                (messageuri, po.nTokens,      size_tokens),
                (messageuri, po.nSentences,   size_sentences),
                ]
        urls = self.regex_url.findall(messagetext)
        for url in urls:
            triples+=[
                     (messageuri,po.hasUrl,url),
                     ]
        self.size_chars_overall+=[size_chars]
        self.size_tokens_overall+=[size_tokens]
        self.size_sentences_overall+=[size_sentences]
        return triples
    def writeTranslates(self,mode="full"):
        c("mode full or chunk or multigraph write:",mode)
        if mode=="full":
            g=P.context(self.translation_graph)
            self.translation_ttl=self.snapshotid+"Translation.ttl"
            self.translation_xml=self.snapshotid+"Translation.rdf"
            g.serialize(self.final_path_+self.translation_ttl,"turtle"); c("ttl")
            g.serialize(self.final_path_+self.translation_xml,"xml")
            self.size_ttl=os.path.getsize(self.final_path_+self.translation_ttl)/10**6
            self.size_xml=os.path.getsize(self.final_path_+self.translation_xml)/10**6
            self.ntranslation_triples=len(g)
        elif mode=="chunk":
            # writeByChunks
            raise NotImplementedError("Perform P.utils.writeByChunks on self.translation_graph")
        elif mode=="multigraph":
            raise NotImplementedError("Perform serialize(write) on each of the self.translation_graphs")


