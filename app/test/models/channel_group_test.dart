import 'package:flutter_test/flutter_test.dart';
import 'package:app/data/models/channel.dart';
import 'package:app/data/models/channel_group.dart';

void main() {
  group('ChannelGroup', () {
    test('count returns the number of channels', () {
      const group = ChannelGroup(
        name: 'BR Abertos',
        channels: [
          Channel(name: 'Globo', url: 'http://globo'),
          Channel(name: 'SBT', url: 'http://sbt'),
          Channel(name: 'Record', url: 'http://record'),
        ],
      );

      expect(group.count, 3);
    });

    test('count returns 0 for empty channel list', () {
      const group = ChannelGroup(name: 'Vazio', channels: []);
      expect(group.count, 0);
    });

    test('name is stored correctly', () {
      const group = ChannelGroup(name: 'BR Esportes', channels: []);
      expect(group.name, 'BR Esportes');
    });
  });
}
