import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

class PlaylistRemoteDatasource {
  static const int _maxRetries = 3;
  static const Duration _timeout = Duration(seconds: 15);

  Future<String> fetchPlaylist(String url) async {
    Exception? lastError;

    for (int attempt = 1; attempt <= _maxRetries; attempt++) {
      try {
        // Try standard http first
        final response = await http
            .get(Uri.parse(url))
            .timeout(_timeout);
        if (response.statusCode == 200) {
          return response.body;
        }
        lastError = Exception('HTTP ${response.statusCode}');
      } on HandshakeException catch (e) {
        // SSL handshake failed — try with relaxed SSL
        try {
          return await _fetchWithRelaxedSsl(url);
        } catch (sslRetryError) {
          lastError = Exception('SSL error: $e');
        }
      } on SocketException catch (e) {
        lastError = Exception('Network error: $e');
      } on HttpException catch (e) {
        lastError = Exception('HTTP error: $e');
      } catch (e) {
        lastError = Exception('$e');
      }

      // Wait before retrying (exponential backoff: 1s, 2s, 4s)
      if (attempt < _maxRetries) {
        await Future.delayed(Duration(seconds: 1 << (attempt - 1)));
      }
    }

    throw Exception(
        'Failed to load playlist after $_maxRetries attempts: $lastError');
  }

  /// Fallback: use dart:io HttpClient with relaxed SSL validation
  Future<String> _fetchWithRelaxedSsl(String url) async {
    final httpClient = HttpClient();
    httpClient.badCertificateCallback = (cert, host, port) => true;
    httpClient.connectionTimeout = _timeout;

    try {
      final request = await httpClient.getUrl(Uri.parse(url));
      final response = await request.close().timeout(_timeout);

      if (response.statusCode == 200) {
        return await response.transform(utf8.decoder).join();
      }
      throw Exception('HTTP ${response.statusCode}');
    } finally {
      httpClient.close();
    }
  }
}

