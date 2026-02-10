import 'package:flutter_test/flutter_test.dart';
import 'package:app/core/constants/app_constants.dart';

void main() {
  group('AppConstants', () {
    test('appName is IPTV Player', () {
      expect(AppConstants.appName, 'IPTV Player');
    });

    test('defaultPlaylistUrl points to GitHub raw content', () {
      expect(
        AppConstants.defaultPlaylistUrl,
        contains('raw.githubusercontent.com'),
      );
      expect(AppConstants.defaultPlaylistUrl, endsWith('playlist.m3u'));
    });

    test('playlistCacheDuration is 6 hours', () {
      expect(
        AppConstants.playlistCacheDuration,
        const Duration(hours: 6),
      );
    });

    test('desktopBreakpoint is 800', () {
      expect(AppConstants.desktopBreakpoint, 800);
    });

    test('tabletBreakpoint is 600', () {
      expect(AppConstants.tabletBreakpoint, 600);
    });

    test('desktopBreakpoint > tabletBreakpoint', () {
      expect(
        AppConstants.desktopBreakpoint,
        greaterThan(AppConstants.tabletBreakpoint),
      );
    });
  });
}
