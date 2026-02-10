import 'package:flutter_test/flutter_test.dart';
import 'package:app/data/parsers/m3u_parser.dart';

void main() {
  group('M3uParser.parse', () {
    test('returns empty list for empty string', () {
      expect(M3uParser.parse(''), isEmpty);
    });

    test('returns empty list for header-only content', () {
      expect(M3uParser.parse('#EXTM3U'), isEmpty);
    });

    test('parses single channel with all attributes', () {
      const content = '''
#EXTM3U
#EXTINF:-1 tvg-id="globo.br" tvg-name="TV Globo" tvg-logo="http://logo.png" group-title="BR Abertos" tvg-chno="4",Globo
http://stream.example.com/globo
''';

      final channels = M3uParser.parse(content);

      expect(channels, hasLength(1));
      expect(channels[0].name, 'Globo');
      expect(channels[0].url, 'http://stream.example.com/globo');
      expect(channels[0].group, 'BR Abertos');
      expect(channels[0].logoUrl, 'http://logo.png');
      expect(channels[0].tvgId, 'globo.br');
      expect(channels[0].tvgName, 'TV Globo');
      expect(channels[0].tvgChno, '4');
    });

    test('parses channel with channel-number attribute as tvgChno', () {
      const content = '''
#EXTM3U
#EXTINF:-1 channel-number="7",Band
http://stream.example.com/band
''';

      final channels = M3uParser.parse(content);

      expect(channels, hasLength(1));
      expect(channels[0].tvgChno, '7');
    });

    test('parses multiple channels', () {
      const content = '''
#EXTM3U
#EXTINF:-1 group-title="BR Abertos",Globo
http://stream1.com/globo
#EXTINF:-1 group-title="BR Abertos",SBT
http://stream2.com/sbt
#EXTINF:-1 group-title="BR Esportes",ESPN
http://stream3.com/espn
''';

      final channels = M3uParser.parse(content);

      expect(channels, hasLength(3));
      expect(channels[0].name, 'Globo');
      expect(channels[1].name, 'SBT');
      expect(channels[2].name, 'ESPN');
    });

    test('skips EXTINF without URL', () {
      const content = '''
#EXTM3U
#EXTINF:-1,Canal Sem URL
''';

      final channels = M3uParser.parse(content);
      expect(channels, isEmpty);
    });

    test('channel with no group-title gets empty group', () {
      const content = '''
#EXTM3U
#EXTINF:-1,Canal Livre
http://stream.com/livre
''';

      final channels = M3uParser.parse(content);

      expect(channels, hasLength(1));
      expect(channels[0].group, '');
    });

    test('skips blank lines and comments between EXTINF and URL', () {
      const content = '''
#EXTM3U
#EXTINF:-1 group-title="BR Abertos",Globo

# This is a comment
http://stream.com/globo
''';

      final channels = M3uParser.parse(content);

      expect(channels, hasLength(1));
      expect(channels[0].url, 'http://stream.com/globo');
    });
  });

  group('M3uParser.groupChannels', () {
    test('groups channels by group field', () {
      final channels = M3uParser.parse('''
#EXTM3U
#EXTINF:-1 group-title="BR Abertos",Globo
http://g
#EXTINF:-1 group-title="BR Abertos",SBT
http://s
#EXTINF:-1 group-title="BR Esportes",ESPN
http://e
''');

      final groups = M3uParser.groupChannels(channels);

      expect(groups.length, 2);

      final abertos = groups.firstWhere((g) => g.name == 'BR Abertos');
      final esportes = groups.firstWhere((g) => g.name == 'BR Esportes');

      expect(abertos.count, 2);
      expect(esportes.count, 1);
    });

    test('channels with empty group go to "Outros"', () {
      final channels = M3uParser.parse('''
#EXTM3U
#EXTINF:-1,Canal Livre
http://livre
''');

      final groups = M3uParser.groupChannels(channels);

      expect(groups, hasLength(1));
      expect(groups[0].name, 'Outros');
      expect(groups[0].count, 1);
    });

    test('BR groups are sorted before non-BR groups', () {
      final channels = M3uParser.parse('''
#EXTM3U
#EXTINF:-1 group-title="USA News",CNN
http://cnn
#EXTINF:-1 group-title="BR Esportes",ESPN BR
http://espn
#EXTINF:-1 group-title="BR Abertos",Globo
http://globo
#EXTINF:-1 group-title="UK Entertainment",BBC
http://bbc
''');

      final groups = M3uParser.groupChannels(channels);

      expect(groups.length, 4);
      // BR groups come first
      expect(groups[0].name, startsWith('BR'));
      expect(groups[1].name, startsWith('BR'));
      // Non-BR groups after
      expect(groups[2].name, isNot(startsWith('BR')));
      expect(groups[3].name, isNot(startsWith('BR')));
    });

    test('returns empty list for empty channel list', () {
      final groups = M3uParser.groupChannels([]);
      expect(groups, isEmpty);
    });
  });
}
