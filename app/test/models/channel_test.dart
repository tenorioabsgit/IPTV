import 'package:flutter_test/flutter_test.dart';
import 'package:app/data/models/channel.dart';

void main() {
  group('Channel', () {
    const channel = Channel(
      name: 'Globo',
      url: 'http://example.com/globo?token=abc',
      group: 'BR Abertos',
      logoUrl: 'http://example.com/logo.png',
      tvgId: 'globo.br',
      tvgName: 'TV Globo',
      tvgChno: '4',
    );

    test('toJson() serializes all fields', () {
      final json = channel.toJson();

      expect(json['name'], 'Globo');
      expect(json['url'], 'http://example.com/globo?token=abc');
      expect(json['group'], 'BR Abertos');
      expect(json['logoUrl'], 'http://example.com/logo.png');
      expect(json['tvgId'], 'globo.br');
      expect(json['tvgName'], 'TV Globo');
      expect(json['tvgChno'], '4');
    });

    test('fromJson() deserializes all fields', () {
      final json = {
        'name': 'SBT',
        'url': 'http://example.com/sbt',
        'group': 'BR Abertos',
        'logoUrl': 'http://example.com/sbt.png',
        'tvgId': 'sbt.br',
        'tvgName': 'SBT',
        'tvgChno': '5',
      };

      final ch = Channel.fromJson(json);

      expect(ch.name, 'SBT');
      expect(ch.url, 'http://example.com/sbt');
      expect(ch.group, 'BR Abertos');
      expect(ch.logoUrl, 'http://example.com/sbt.png');
      expect(ch.tvgId, 'sbt.br');
      expect(ch.tvgName, 'SBT');
      expect(ch.tvgChno, '5');
    });

    test('fromJson() handles null optional fields', () {
      final json = {
        'name': 'Canal Teste',
        'url': 'http://example.com/teste',
      };

      final ch = Channel.fromJson(json);

      expect(ch.name, 'Canal Teste');
      expect(ch.url, 'http://example.com/teste');
      expect(ch.group, '');
      expect(ch.logoUrl, isNull);
      expect(ch.tvgId, isNull);
      expect(ch.tvgName, isNull);
      expect(ch.tvgChno, isNull);
    });

    test('toJson/fromJson roundtrip preserves data', () {
      final restored = Channel.fromJson(channel.toJson());

      expect(restored.name, channel.name);
      expect(restored.url, channel.url);
      expect(restored.group, channel.group);
      expect(restored.logoUrl, channel.logoUrl);
      expect(restored.tvgId, channel.tvgId);
      expect(restored.tvgName, channel.tvgName);
      expect(restored.tvgChno, channel.tvgChno);
    });

    test('uniqueId strips query parameters from url', () {
      expect(channel.uniqueId, 'http://example.com/globo');
    });

    test('uniqueId returns full url when no query params', () {
      const ch = Channel(name: 'Test', url: 'http://example.com/stream');
      expect(ch.uniqueId, 'http://example.com/stream');
    });

    test('equality is based on url', () {
      const ch1 = Channel(name: 'Globo', url: 'http://example.com/globo');
      const ch2 = Channel(name: 'Globo HD', url: 'http://example.com/globo');
      const ch3 = Channel(name: 'Globo', url: 'http://example.com/other');

      expect(ch1, equals(ch2));
      expect(ch1, isNot(equals(ch3)));
    });

    test('hashCode is based on url', () {
      const ch1 = Channel(name: 'A', url: 'http://same');
      const ch2 = Channel(name: 'B', url: 'http://same');

      expect(ch1.hashCode, ch2.hashCode);
    });

    test('default group is empty string', () {
      const ch = Channel(name: 'Test', url: 'http://test');
      expect(ch.group, '');
    });
  });
}
