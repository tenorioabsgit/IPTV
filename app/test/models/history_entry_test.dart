import 'package:flutter_test/flutter_test.dart';
import 'package:app/data/models/channel.dart';
import 'package:app/data/repositories/history_repository.dart';

void main() {
  group('HistoryEntry', () {
    final watchedAt = DateTime(2026, 2, 9, 20, 0, 0);
    const channel = Channel(
      name: 'ESPN',
      url: 'http://example.com/espn',
      group: 'BR Esportes',
      logoUrl: 'http://example.com/espn.png',
    );

    final entry = HistoryEntry(channel: channel, watchedAt: watchedAt);

    test('toJson() serializes channel and watchedAt', () {
      final json = entry.toJson();

      expect(json['channel'], isA<Map<String, dynamic>>());
      expect(json['channel']['name'], 'ESPN');
      expect(json['channel']['url'], 'http://example.com/espn');
      expect(json['watchedAt'], watchedAt.toIso8601String());
    });

    test('fromJson() deserializes correctly', () {
      final json = {
        'channel': {
          'name': 'SporTV',
          'url': 'http://example.com/sportv',
          'group': 'BR Esportes',
        },
        'watchedAt': '2026-01-15T10:30:00.000',
      };

      final restored = HistoryEntry.fromJson(json);

      expect(restored.channel.name, 'SporTV');
      expect(restored.channel.url, 'http://example.com/sportv');
      expect(restored.watchedAt, DateTime(2026, 1, 15, 10, 30, 0));
    });

    test('toJson/fromJson roundtrip preserves data', () {
      final json = entry.toJson();
      final restored = HistoryEntry.fromJson(json);

      expect(restored.channel.name, entry.channel.name);
      expect(restored.channel.url, entry.channel.url);
      expect(restored.channel.group, entry.channel.group);
      expect(restored.channel.logoUrl, entry.channel.logoUrl);
      expect(restored.watchedAt, entry.watchedAt);
    });
  });
}
