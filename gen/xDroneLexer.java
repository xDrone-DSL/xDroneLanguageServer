// Generated from C:/Users/jxzk1/Desktop/xdrone-dsl/flask-backend/antlr\xDroneLexer.g4 by ANTLR 4.9.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class xDroneLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		MAIN=1, TAKEOFF=2, LAND=3, UP=4, DOWN=5, LEFT=6, RIGHT=7, FORWARD=8, BACKWARD=9, 
		ROTATE_LEFT=10, ROTATE_RIGHT=11, WAIT=12, AT=13, INSERT=14, REMOVE=15, 
		SIZE=16, IF=17, ELSE=18, WHILE=19, FOR=20, FROM=21, TO=22, STEP=23, REPEAT=24, 
		TIMES=25, DEL=26, FUNCTION=27, PROCEDURE=28, RETURN=29, TYPE_INT=30, TYPE_DECIMAL=31, 
		TYPE_STRING=32, TYPE_BOOLEAN=33, TYPE_VECTOR=34, TYPE_DRONE=35, TYPE_LIST=36, 
		TRUE=37, FALSE=38, VEC_X=39, VEC_Y=40, VEC_Z=41, MULTI=42, DIV=43, PLUS=44, 
		MINUS=45, CONCAT=46, GREATER=47, GREATER_EQ=48, LESS=49, LESS_EQ=50, EQ=51, 
		NOT_EQ=52, NOT=53, AND=54, OR=55, L_PAR=56, R_PAR=57, L_BRACKET=58, R_BRACKET=59, 
		L_BRACE=60, R_BRACE=61, DOT=62, COMMA=63, SEMICOLON=64, ARROW=65, PARALLEL=66, 
		COMMENT=67, WS=68, IDENT=69, INT=70, FLOAT=71, ESCAPED_STRING=72;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"MAIN", "TAKEOFF", "LAND", "UP", "DOWN", "LEFT", "RIGHT", "FORWARD", 
			"BACKWARD", "ROTATE_LEFT", "ROTATE_RIGHT", "WAIT", "AT", "INSERT", "REMOVE", 
			"SIZE", "IF", "ELSE", "WHILE", "FOR", "FROM", "TO", "STEP", "REPEAT", 
			"TIMES", "DEL", "FUNCTION", "PROCEDURE", "RETURN", "TYPE_INT", "TYPE_DECIMAL", 
			"TYPE_STRING", "TYPE_BOOLEAN", "TYPE_VECTOR", "TYPE_DRONE", "TYPE_LIST", 
			"TRUE", "FALSE", "VEC_X", "VEC_Y", "VEC_Z", "MULTI", "DIV", "PLUS", "MINUS", 
			"CONCAT", "GREATER", "GREATER_EQ", "LESS", "LESS_EQ", "EQ", "NOT_EQ", 
			"NOT", "AND", "OR", "L_PAR", "R_PAR", "L_BRACKET", "R_BRACKET", "L_BRACE", 
			"R_BRACE", "DOT", "COMMA", "SEMICOLON", "ARROW", "PARALLEL", "DIGIT", 
			"LOWERCASE", "UPPERCASE", "UNDERSCORE", "COMMENT", "WS", "IDENT", "INT", 
			"SIGNED_INT", "DECIMAL", "EXP", "FLOAT", "DOUBLE_QUOTE", "ESCAPED_CHAR", 
			"CHARACTER", "ESCAPED_STRING"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'main'", "'takeoff'", "'land'", "'up'", "'down'", "'left'", "'right'", 
			"'forward'", "'backward'", "'rotate_left'", "'rotate_right'", "'wait'", 
			"'at'", "'insert'", "'remove'", "'size'", "'if'", "'else'", "'while'", 
			"'for'", "'from'", "'to'", "'step'", "'repeat'", "'times'", "'del'", 
			"'function'", "'procedure'", "'return'", "'int'", "'decimal'", "'string'", 
			"'boolean'", "'vector'", "'drone'", "'list'", "'true'", "'false'", "'x'", 
			"'y'", "'z'", "'*'", "'/'", "'+'", "'-'", "'&'", "'>'", "'>='", "'<'", 
			"'<='", "'=='", "'=/='", "'not'", "'and'", "'or'", "'('", "')'", "'['", 
			"']'", "'{'", "'}'", "'.'", "','", "';'", "'<-'", "'||'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "MAIN", "TAKEOFF", "LAND", "UP", "DOWN", "LEFT", "RIGHT", "FORWARD", 
			"BACKWARD", "ROTATE_LEFT", "ROTATE_RIGHT", "WAIT", "AT", "INSERT", "REMOVE", 
			"SIZE", "IF", "ELSE", "WHILE", "FOR", "FROM", "TO", "STEP", "REPEAT", 
			"TIMES", "DEL", "FUNCTION", "PROCEDURE", "RETURN", "TYPE_INT", "TYPE_DECIMAL", 
			"TYPE_STRING", "TYPE_BOOLEAN", "TYPE_VECTOR", "TYPE_DRONE", "TYPE_LIST", 
			"TRUE", "FALSE", "VEC_X", "VEC_Y", "VEC_Z", "MULTI", "DIV", "PLUS", "MINUS", 
			"CONCAT", "GREATER", "GREATER_EQ", "LESS", "LESS_EQ", "EQ", "NOT_EQ", 
			"NOT", "AND", "OR", "L_PAR", "R_PAR", "L_BRACKET", "R_BRACKET", "L_BRACE", 
			"R_BRACE", "DOT", "COMMA", "SEMICOLON", "ARROW", "PARALLEL", "COMMENT", 
			"WS", "IDENT", "INT", "FLOAT", "ESCAPED_STRING"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public xDroneLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "xDroneLexer.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2J\u023f\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t"+
		"\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t="+
		"\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I"+
		"\tI\4J\tJ\4K\tK\4L\tL\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\3\2\3"+
		"\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\5"+
		"\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3"+
		"\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n"+
		"\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3"+
		"\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3"+
		"\16\3\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3"+
		"\20\3\20\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3"+
		"\23\3\24\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3"+
		"\26\3\26\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3"+
		"\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3"+
		"\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3"+
		"\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3"+
		"\37\3 \3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3"+
		"\"\3\"\3\"\3#\3#\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&\3"+
		"&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3)\3)\3*\3*\3+\3+\3,\3,\3-\3"+
		"-\3.\3.\3/\3/\3\60\3\60\3\61\3\61\3\61\3\62\3\62\3\63\3\63\3\63\3\64\3"+
		"\64\3\64\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67\3\67\3\67\3\67\3"+
		"8\38\38\39\39\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3A\3A\3B\3B\3"+
		"B\3C\3C\3C\3D\3D\3E\3E\3F\3F\3G\3G\3H\3H\7H\u01e2\nH\fH\16H\u01e5\13H"+
		"\3H\3H\3H\3H\3I\6I\u01ec\nI\rI\16I\u01ed\3I\3I\3J\3J\3J\5J\u01f5\nJ\3"+
		"J\3J\3J\3J\7J\u01fb\nJ\fJ\16J\u01fe\13J\3K\6K\u0201\nK\rK\16K\u0202\3"+
		"L\5L\u0206\nL\3L\3L\3M\3M\3M\5M\u020d\nM\3M\3M\5M\u0211\nM\3N\3N\3N\3"+
		"O\3O\3O\3O\3O\5O\u021b\nO\5O\u021d\nO\3P\3P\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3"+
		"Q\3Q\3Q\3Q\3Q\3Q\3Q\3Q\5Q\u0231\nQ\3R\3R\5R\u0235\nR\3S\3S\7S\u0239\n"+
		"S\fS\16S\u023c\13S\3S\3S\2\2T\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13"+
		"\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61"+
		"\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61"+
		"a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081B\u0083C\u0085D\u0087"+
		"\2\u0089\2\u008b\2\u008d\2\u008fE\u0091F\u0093G\u0095H\u0097\2\u0099\2"+
		"\u009b\2\u009dI\u009f\2\u00a1\2\u00a3\2\u00a5J\3\2\n\3\2\62;\3\2c|\3\2"+
		"C\\\4\2\f\f\17\17\5\2\13\f\17\17\"\"\4\2--//\4\2GGgg\5\2$$))^^\2\u024b"+
		"\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2"+
		"\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2"+
		"\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2"+
		"\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2"+
		"\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3"+
		"\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2"+
		"\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2"+
		"U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3"+
		"\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2"+
		"\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2"+
		"{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085"+
		"\3\2\2\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2"+
		"\2\2\u009d\3\2\2\2\2\u00a5\3\2\2\2\3\u00a7\3\2\2\2\5\u00ac\3\2\2\2\7\u00b4"+
		"\3\2\2\2\t\u00b9\3\2\2\2\13\u00bc\3\2\2\2\r\u00c1\3\2\2\2\17\u00c6\3\2"+
		"\2\2\21\u00cc\3\2\2\2\23\u00d4\3\2\2\2\25\u00dd\3\2\2\2\27\u00e9\3\2\2"+
		"\2\31\u00f6\3\2\2\2\33\u00fb\3\2\2\2\35\u00fe\3\2\2\2\37\u0105\3\2\2\2"+
		"!\u010c\3\2\2\2#\u0111\3\2\2\2%\u0114\3\2\2\2\'\u0119\3\2\2\2)\u011f\3"+
		"\2\2\2+\u0123\3\2\2\2-\u0128\3\2\2\2/\u012b\3\2\2\2\61\u0130\3\2\2\2\63"+
		"\u0137\3\2\2\2\65\u013d\3\2\2\2\67\u0141\3\2\2\29\u014a\3\2\2\2;\u0154"+
		"\3\2\2\2=\u015b\3\2\2\2?\u015f\3\2\2\2A\u0167\3\2\2\2C\u016e\3\2\2\2E"+
		"\u0176\3\2\2\2G\u017d\3\2\2\2I\u0183\3\2\2\2K\u0188\3\2\2\2M\u018d\3\2"+
		"\2\2O\u0193\3\2\2\2Q\u0195\3\2\2\2S\u0197\3\2\2\2U\u0199\3\2\2\2W\u019b"+
		"\3\2\2\2Y\u019d\3\2\2\2[\u019f\3\2\2\2]\u01a1\3\2\2\2_\u01a3\3\2\2\2a"+
		"\u01a5\3\2\2\2c\u01a8\3\2\2\2e\u01aa\3\2\2\2g\u01ad\3\2\2\2i\u01b0\3\2"+
		"\2\2k\u01b4\3\2\2\2m\u01b8\3\2\2\2o\u01bc\3\2\2\2q\u01bf\3\2\2\2s\u01c1"+
		"\3\2\2\2u\u01c3\3\2\2\2w\u01c5\3\2\2\2y\u01c7\3\2\2\2{\u01c9\3\2\2\2}"+
		"\u01cb\3\2\2\2\177\u01cd\3\2\2\2\u0081\u01cf\3\2\2\2\u0083\u01d1\3\2\2"+
		"\2\u0085\u01d4\3\2\2\2\u0087\u01d7\3\2\2\2\u0089\u01d9\3\2\2\2\u008b\u01db"+
		"\3\2\2\2\u008d\u01dd\3\2\2\2\u008f\u01df\3\2\2\2\u0091\u01eb\3\2\2\2\u0093"+
		"\u01f4\3\2\2\2\u0095\u0200\3\2\2\2\u0097\u0205\3\2\2\2\u0099\u0210\3\2"+
		"\2\2\u009b\u0212\3\2\2\2\u009d\u021c\3\2\2\2\u009f\u021e\3\2\2\2\u00a1"+
		"\u0230\3\2\2\2\u00a3\u0234\3\2\2\2\u00a5\u0236\3\2\2\2\u00a7\u00a8\7o"+
		"\2\2\u00a8\u00a9\7c\2\2\u00a9\u00aa\7k\2\2\u00aa\u00ab\7p\2\2\u00ab\4"+
		"\3\2\2\2\u00ac\u00ad\7v\2\2\u00ad\u00ae\7c\2\2\u00ae\u00af\7m\2\2\u00af"+
		"\u00b0\7g\2\2\u00b0\u00b1\7q\2\2\u00b1\u00b2\7h\2\2\u00b2\u00b3\7h\2\2"+
		"\u00b3\6\3\2\2\2\u00b4\u00b5\7n\2\2\u00b5\u00b6\7c\2\2\u00b6\u00b7\7p"+
		"\2\2\u00b7\u00b8\7f\2\2\u00b8\b\3\2\2\2\u00b9\u00ba\7w\2\2\u00ba\u00bb"+
		"\7r\2\2\u00bb\n\3\2\2\2\u00bc\u00bd\7f\2\2\u00bd\u00be\7q\2\2\u00be\u00bf"+
		"\7y\2\2\u00bf\u00c0\7p\2\2\u00c0\f\3\2\2\2\u00c1\u00c2\7n\2\2\u00c2\u00c3"+
		"\7g\2\2\u00c3\u00c4\7h\2\2\u00c4\u00c5\7v\2\2\u00c5\16\3\2\2\2\u00c6\u00c7"+
		"\7t\2\2\u00c7\u00c8\7k\2\2\u00c8\u00c9\7i\2\2\u00c9\u00ca\7j\2\2\u00ca"+
		"\u00cb\7v\2\2\u00cb\20\3\2\2\2\u00cc\u00cd\7h\2\2\u00cd\u00ce\7q\2\2\u00ce"+
		"\u00cf\7t\2\2\u00cf\u00d0\7y\2\2\u00d0\u00d1\7c\2\2\u00d1\u00d2\7t\2\2"+
		"\u00d2\u00d3\7f\2\2\u00d3\22\3\2\2\2\u00d4\u00d5\7d\2\2\u00d5\u00d6\7"+
		"c\2\2\u00d6\u00d7\7e\2\2\u00d7\u00d8\7m\2\2\u00d8\u00d9\7y\2\2\u00d9\u00da"+
		"\7c\2\2\u00da\u00db\7t\2\2\u00db\u00dc\7f\2\2\u00dc\24\3\2\2\2\u00dd\u00de"+
		"\7t\2\2\u00de\u00df\7q\2\2\u00df\u00e0\7v\2\2\u00e0\u00e1\7c\2\2\u00e1"+
		"\u00e2\7v\2\2\u00e2\u00e3\7g\2\2\u00e3\u00e4\7a\2\2\u00e4\u00e5\7n\2\2"+
		"\u00e5\u00e6\7g\2\2\u00e6\u00e7\7h\2\2\u00e7\u00e8\7v\2\2\u00e8\26\3\2"+
		"\2\2\u00e9\u00ea\7t\2\2\u00ea\u00eb\7q\2\2\u00eb\u00ec\7v\2\2\u00ec\u00ed"+
		"\7c\2\2\u00ed\u00ee\7v\2\2\u00ee\u00ef\7g\2\2\u00ef\u00f0\7a\2\2\u00f0"+
		"\u00f1\7t\2\2\u00f1\u00f2\7k\2\2\u00f2\u00f3\7i\2\2\u00f3\u00f4\7j\2\2"+
		"\u00f4\u00f5\7v\2\2\u00f5\30\3\2\2\2\u00f6\u00f7\7y\2\2\u00f7\u00f8\7"+
		"c\2\2\u00f8\u00f9\7k\2\2\u00f9\u00fa\7v\2\2\u00fa\32\3\2\2\2\u00fb\u00fc"+
		"\7c\2\2\u00fc\u00fd\7v\2\2\u00fd\34\3\2\2\2\u00fe\u00ff\7k\2\2\u00ff\u0100"+
		"\7p\2\2\u0100\u0101\7u\2\2\u0101\u0102\7g\2\2\u0102\u0103\7t\2\2\u0103"+
		"\u0104\7v\2\2\u0104\36\3\2\2\2\u0105\u0106\7t\2\2\u0106\u0107\7g\2\2\u0107"+
		"\u0108\7o\2\2\u0108\u0109\7q\2\2\u0109\u010a\7x\2\2\u010a\u010b\7g\2\2"+
		"\u010b \3\2\2\2\u010c\u010d\7u\2\2\u010d\u010e\7k\2\2\u010e\u010f\7|\2"+
		"\2\u010f\u0110\7g\2\2\u0110\"\3\2\2\2\u0111\u0112\7k\2\2\u0112\u0113\7"+
		"h\2\2\u0113$\3\2\2\2\u0114\u0115\7g\2\2\u0115\u0116\7n\2\2\u0116\u0117"+
		"\7u\2\2\u0117\u0118\7g\2\2\u0118&\3\2\2\2\u0119\u011a\7y\2\2\u011a\u011b"+
		"\7j\2\2\u011b\u011c\7k\2\2\u011c\u011d\7n\2\2\u011d\u011e\7g\2\2\u011e"+
		"(\3\2\2\2\u011f\u0120\7h\2\2\u0120\u0121\7q\2\2\u0121\u0122\7t\2\2\u0122"+
		"*\3\2\2\2\u0123\u0124\7h\2\2\u0124\u0125\7t\2\2\u0125\u0126\7q\2\2\u0126"+
		"\u0127\7o\2\2\u0127,\3\2\2\2\u0128\u0129\7v\2\2\u0129\u012a\7q\2\2\u012a"+
		".\3\2\2\2\u012b\u012c\7u\2\2\u012c\u012d\7v\2\2\u012d\u012e\7g\2\2\u012e"+
		"\u012f\7r\2\2\u012f\60\3\2\2\2\u0130\u0131\7t\2\2\u0131\u0132\7g\2\2\u0132"+
		"\u0133\7r\2\2\u0133\u0134\7g\2\2\u0134\u0135\7c\2\2\u0135\u0136\7v\2\2"+
		"\u0136\62\3\2\2\2\u0137\u0138\7v\2\2\u0138\u0139\7k\2\2\u0139\u013a\7"+
		"o\2\2\u013a\u013b\7g\2\2\u013b\u013c\7u\2\2\u013c\64\3\2\2\2\u013d\u013e"+
		"\7f\2\2\u013e\u013f\7g\2\2\u013f\u0140\7n\2\2\u0140\66\3\2\2\2\u0141\u0142"+
		"\7h\2\2\u0142\u0143\7w\2\2\u0143\u0144\7p\2\2\u0144\u0145\7e\2\2\u0145"+
		"\u0146\7v\2\2\u0146\u0147\7k\2\2\u0147\u0148\7q\2\2\u0148\u0149\7p\2\2"+
		"\u01498\3\2\2\2\u014a\u014b\7r\2\2\u014b\u014c\7t\2\2\u014c\u014d\7q\2"+
		"\2\u014d\u014e\7e\2\2\u014e\u014f\7g\2\2\u014f\u0150\7f\2\2\u0150\u0151"+
		"\7w\2\2\u0151\u0152\7t\2\2\u0152\u0153\7g\2\2\u0153:\3\2\2\2\u0154\u0155"+
		"\7t\2\2\u0155\u0156\7g\2\2\u0156\u0157\7v\2\2\u0157\u0158\7w\2\2\u0158"+
		"\u0159\7t\2\2\u0159\u015a\7p\2\2\u015a<\3\2\2\2\u015b\u015c\7k\2\2\u015c"+
		"\u015d\7p\2\2\u015d\u015e\7v\2\2\u015e>\3\2\2\2\u015f\u0160\7f\2\2\u0160"+
		"\u0161\7g\2\2\u0161\u0162\7e\2\2\u0162\u0163\7k\2\2\u0163\u0164\7o\2\2"+
		"\u0164\u0165\7c\2\2\u0165\u0166\7n\2\2\u0166@\3\2\2\2\u0167\u0168\7u\2"+
		"\2\u0168\u0169\7v\2\2\u0169\u016a\7t\2\2\u016a\u016b\7k\2\2\u016b\u016c"+
		"\7p\2\2\u016c\u016d\7i\2\2\u016dB\3\2\2\2\u016e\u016f\7d\2\2\u016f\u0170"+
		"\7q\2\2\u0170\u0171\7q\2\2\u0171\u0172\7n\2\2\u0172\u0173\7g\2\2\u0173"+
		"\u0174\7c\2\2\u0174\u0175\7p\2\2\u0175D\3\2\2\2\u0176\u0177\7x\2\2\u0177"+
		"\u0178\7g\2\2\u0178\u0179\7e\2\2\u0179\u017a\7v\2\2\u017a\u017b\7q\2\2"+
		"\u017b\u017c\7t\2\2\u017cF\3\2\2\2\u017d\u017e\7f\2\2\u017e\u017f\7t\2"+
		"\2\u017f\u0180\7q\2\2\u0180\u0181\7p\2\2\u0181\u0182\7g\2\2\u0182H\3\2"+
		"\2\2\u0183\u0184\7n\2\2\u0184\u0185\7k\2\2\u0185\u0186\7u\2\2\u0186\u0187"+
		"\7v\2\2\u0187J\3\2\2\2\u0188\u0189\7v\2\2\u0189\u018a\7t\2\2\u018a\u018b"+
		"\7w\2\2\u018b\u018c\7g\2\2\u018cL\3\2\2\2\u018d\u018e\7h\2\2\u018e\u018f"+
		"\7c\2\2\u018f\u0190\7n\2\2\u0190\u0191\7u\2\2\u0191\u0192\7g\2\2\u0192"+
		"N\3\2\2\2\u0193\u0194\7z\2\2\u0194P\3\2\2\2\u0195\u0196\7{\2\2\u0196R"+
		"\3\2\2\2\u0197\u0198\7|\2\2\u0198T\3\2\2\2\u0199\u019a\7,\2\2\u019aV\3"+
		"\2\2\2\u019b\u019c\7\61\2\2\u019cX\3\2\2\2\u019d\u019e\7-\2\2\u019eZ\3"+
		"\2\2\2\u019f\u01a0\7/\2\2\u01a0\\\3\2\2\2\u01a1\u01a2\7(\2\2\u01a2^\3"+
		"\2\2\2\u01a3\u01a4\7@\2\2\u01a4`\3\2\2\2\u01a5\u01a6\7@\2\2\u01a6\u01a7"+
		"\7?\2\2\u01a7b\3\2\2\2\u01a8\u01a9\7>\2\2\u01a9d\3\2\2\2\u01aa\u01ab\7"+
		">\2\2\u01ab\u01ac\7?\2\2\u01acf\3\2\2\2\u01ad\u01ae\7?\2\2\u01ae\u01af"+
		"\7?\2\2\u01afh\3\2\2\2\u01b0\u01b1\7?\2\2\u01b1\u01b2\7\61\2\2\u01b2\u01b3"+
		"\7?\2\2\u01b3j\3\2\2\2\u01b4\u01b5\7p\2\2\u01b5\u01b6\7q\2\2\u01b6\u01b7"+
		"\7v\2\2\u01b7l\3\2\2\2\u01b8\u01b9\7c\2\2\u01b9\u01ba\7p\2\2\u01ba\u01bb"+
		"\7f\2\2\u01bbn\3\2\2\2\u01bc\u01bd\7q\2\2\u01bd\u01be\7t\2\2\u01bep\3"+
		"\2\2\2\u01bf\u01c0\7*\2\2\u01c0r\3\2\2\2\u01c1\u01c2\7+\2\2\u01c2t\3\2"+
		"\2\2\u01c3\u01c4\7]\2\2\u01c4v\3\2\2\2\u01c5\u01c6\7_\2\2\u01c6x\3\2\2"+
		"\2\u01c7\u01c8\7}\2\2\u01c8z\3\2\2\2\u01c9\u01ca\7\177\2\2\u01ca|\3\2"+
		"\2\2\u01cb\u01cc\7\60\2\2\u01cc~\3\2\2\2\u01cd\u01ce\7.\2\2\u01ce\u0080"+
		"\3\2\2\2\u01cf\u01d0\7=\2\2\u01d0\u0082\3\2\2\2\u01d1\u01d2\7>\2\2\u01d2"+
		"\u01d3\7/\2\2\u01d3\u0084\3\2\2\2\u01d4\u01d5\7~\2\2\u01d5\u01d6\7~\2"+
		"\2\u01d6\u0086\3\2\2\2\u01d7\u01d8\t\2\2\2\u01d8\u0088\3\2\2\2\u01d9\u01da"+
		"\t\3\2\2\u01da\u008a\3\2\2\2\u01db\u01dc\t\4\2\2\u01dc\u008c\3\2\2\2\u01dd"+
		"\u01de\7a\2\2\u01de\u008e\3\2\2\2\u01df\u01e3\7%\2\2\u01e0\u01e2\n\5\2"+
		"\2\u01e1\u01e0\3\2\2\2\u01e2\u01e5\3\2\2\2\u01e3\u01e1\3\2\2\2\u01e3\u01e4"+
		"\3\2\2\2\u01e4\u01e6\3\2\2\2\u01e5\u01e3\3\2\2\2\u01e6\u01e7\t\5\2\2\u01e7"+
		"\u01e8\3\2\2\2\u01e8\u01e9\bH\2\2\u01e9\u0090\3\2\2\2\u01ea\u01ec\t\6"+
		"\2\2\u01eb\u01ea\3\2\2\2\u01ec\u01ed\3\2\2\2\u01ed\u01eb\3\2\2\2\u01ed"+
		"\u01ee\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef\u01f0\bI\2\2\u01f0\u0092\3\2"+
		"\2\2\u01f1\u01f5\5\u008dG\2\u01f2\u01f5\5\u0089E\2\u01f3\u01f5\5\u008b"+
		"F\2\u01f4\u01f1\3\2\2\2\u01f4\u01f2\3\2\2\2\u01f4\u01f3\3\2\2\2\u01f5"+
		"\u01fc\3\2\2\2\u01f6\u01fb\5\u008dG\2\u01f7\u01fb\5\u0089E\2\u01f8\u01fb"+
		"\5\u008bF\2\u01f9\u01fb\5\u0087D\2\u01fa\u01f6\3\2\2\2\u01fa\u01f7\3\2"+
		"\2\2\u01fa\u01f8\3\2\2\2\u01fa\u01f9\3\2\2\2\u01fb\u01fe\3\2\2\2\u01fc"+
		"\u01fa\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd\u0094\3\2\2\2\u01fe\u01fc\3\2"+
		"\2\2\u01ff\u0201\5\u0087D\2\u0200\u01ff\3\2\2\2\u0201\u0202\3\2\2\2\u0202"+
		"\u0200\3\2\2\2\u0202\u0203\3\2\2\2\u0203\u0096\3\2\2\2\u0204\u0206\t\7"+
		"\2\2\u0205\u0204\3\2\2\2\u0205\u0206\3\2\2\2\u0206\u0207\3\2\2\2\u0207"+
		"\u0208\5\u0095K\2\u0208\u0098\3\2\2\2\u0209\u020a\5\u0095K\2\u020a\u020c"+
		"\7\60\2\2\u020b\u020d\5\u0095K\2\u020c\u020b\3\2\2\2\u020c\u020d\3\2\2"+
		"\2\u020d\u0211\3\2\2\2\u020e\u020f\7\60\2\2\u020f\u0211\5\u0095K\2\u0210"+
		"\u0209\3\2\2\2\u0210\u020e\3\2\2\2\u0211\u009a\3\2\2\2\u0212\u0213\t\b"+
		"\2\2\u0213\u0214\5\u0097L\2\u0214\u009c\3\2\2\2\u0215\u0216\5\u0095K\2"+
		"\u0216\u0217\5\u009bN\2\u0217\u021d\3\2\2\2\u0218\u021a\5\u0099M\2\u0219"+
		"\u021b\5\u009bN\2\u021a\u0219\3\2\2\2\u021a\u021b\3\2\2\2\u021b\u021d"+
		"\3\2\2\2\u021c\u0215\3\2\2\2\u021c\u0218\3\2\2\2\u021d\u009e\3\2\2\2\u021e"+
		"\u021f\7$\2\2\u021f\u00a0\3\2\2\2\u0220\u0221\7^\2\2\u0221\u0231\7\62"+
		"\2\2\u0222\u0223\7^\2\2\u0223\u0231\7d\2\2\u0224\u0225\7^\2\2\u0225\u0231"+
		"\7p\2\2\u0226\u0227\7^\2\2\u0227\u0231\7h\2\2\u0228\u0229\7^\2\2\u0229"+
		"\u0231\7t\2\2\u022a\u022b\7^\2\2\u022b\u0231\5\u009fP\2\u022c\u022d\7"+
		"^\2\2\u022d\u0231\7)\2\2\u022e\u022f\7^\2\2\u022f\u0231\7^\2\2\u0230\u0220"+
		"\3\2\2\2\u0230\u0222\3\2\2\2\u0230\u0224\3\2\2\2\u0230\u0226\3\2\2\2\u0230"+
		"\u0228\3\2\2\2\u0230\u022a\3\2\2\2\u0230\u022c\3\2\2\2\u0230\u022e\3\2"+
		"\2\2\u0231\u00a2\3\2\2\2\u0232\u0235\n\t\2\2\u0233\u0235\5\u00a1Q\2\u0234"+
		"\u0232\3\2\2\2\u0234\u0233\3\2\2\2\u0235\u00a4\3\2\2\2\u0236\u023a\5\u009f"+
		"P\2\u0237\u0239\5\u00a3R\2\u0238\u0237\3\2\2\2\u0239\u023c\3\2\2\2\u023a"+
		"\u0238\3\2\2\2\u023a\u023b\3\2\2\2\u023b\u023d\3\2\2\2\u023c\u023a\3\2"+
		"\2\2\u023d\u023e\5\u009fP\2\u023e\u00a6\3\2\2\2\21\2\u01e3\u01ed\u01f4"+
		"\u01fa\u01fc\u0202\u0205\u020c\u0210\u021a\u021c\u0230\u0234\u023a\3\b"+
		"\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}