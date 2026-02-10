import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:app/core/theme/app_theme.dart';

void main() {
  group('AppTheme', () {
    test('lightTheme is a ThemeData', () {
      expect(AppTheme.lightTheme, isNotNull);
      expect(AppTheme.lightTheme.brightness, Brightness.light);
    });

    test('darkTheme is a ThemeData', () {
      expect(AppTheme.darkTheme, isNotNull);
      expect(AppTheme.darkTheme.brightness, Brightness.dark);
    });

    test('darkTheme uses Material 3', () {
      expect(AppTheme.darkTheme.useMaterial3, isTrue);
    });

    test('lightTheme uses Material 3', () {
      expect(AppTheme.lightTheme.useMaterial3, isTrue);
    });
  });
}
