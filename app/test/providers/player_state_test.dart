import 'package:flutter_test/flutter_test.dart';
import 'package:app/data/models/channel.dart';
import 'package:app/providers/player_provider.dart';

void main() {
  group('PlayerState', () {
    test('default values are correct', () {
      const state = PlayerState();

      expect(state.currentChannel, isNull);
      expect(state.isPlaying, false);
      expect(state.isBuffering, false);
      expect(state.isFullScreen, false);
      expect(state.error, isNull);
    });

    test('copyWith updates only specified fields', () {
      const state = PlayerState();
      final updated = state.copyWith(isPlaying: true);

      expect(updated.isPlaying, true);
      expect(updated.isBuffering, false);
      expect(updated.isFullScreen, false);
      expect(updated.currentChannel, isNull);
      expect(updated.error, isNull);
    });

    test('copyWith preserves existing channel', () {
      const channel = Channel(name: 'Globo', url: 'http://globo');
      const state = PlayerState(currentChannel: channel);
      final updated = state.copyWith(isBuffering: true);

      expect(updated.currentChannel?.name, 'Globo');
      expect(updated.isBuffering, true);
    });

    test('copyWith can update channel', () {
      const ch1 = Channel(name: 'Globo', url: 'http://globo');
      const ch2 = Channel(name: 'SBT', url: 'http://sbt');
      const state = PlayerState(currentChannel: ch1);
      final updated = state.copyWith(currentChannel: ch2);

      expect(updated.currentChannel?.name, 'SBT');
    });

    test('copyWith sets error', () {
      const state = PlayerState();
      final updated = state.copyWith(error: 'Connection failed');

      expect(updated.error, 'Connection failed');
    });

    test('copyWith clearError removes existing error', () {
      const state = PlayerState(error: 'Some error');
      final updated = state.copyWith(clearError: true);

      expect(updated.error, isNull);
    });

    test('copyWith clearError takes precedence over error arg', () {
      const state = PlayerState(error: 'Old error');
      final updated = state.copyWith(
        error: 'New error',
        clearError: true,
      );

      expect(updated.error, isNull);
    });

    test('copyWith preserves error when clearError is false', () {
      const state = PlayerState(error: 'Existing error');
      final updated = state.copyWith(isPlaying: true);

      expect(updated.error, 'Existing error');
      expect(updated.isPlaying, true);
    });

    test('copyWith can toggle fullscreen', () {
      const state = PlayerState(isFullScreen: false);
      final updated = state.copyWith(isFullScreen: true);

      expect(updated.isFullScreen, true);
    });

    test('multiple copyWith chains preserve state correctly', () {
      const channel = Channel(name: 'ESPN', url: 'http://espn');
      const state = PlayerState();

      final s1 = state.copyWith(currentChannel: channel);
      final s2 = s1.copyWith(isBuffering: true);
      final s3 = s2.copyWith(isPlaying: true, isBuffering: false);

      expect(s3.currentChannel?.name, 'ESPN');
      expect(s3.isPlaying, true);
      expect(s3.isBuffering, false);
      expect(s3.isFullScreen, false);
      expect(s3.error, isNull);
    });
  });
}
