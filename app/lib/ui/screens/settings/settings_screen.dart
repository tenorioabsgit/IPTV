import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/constants/app_constants.dart';
import '../../../providers/playlist_provider.dart';
import '../../../providers/settings_provider.dart';
import '../../../providers/player_provider.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  late final TextEditingController _urlController;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController(
      text: ref.read(playlistUrlProvider),
    );
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = ref.watch(darkModeProvider);
    final colors = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('Configurações')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Appearance
          _SectionTitle(text: 'Aparência', color: colors.primary),
          const SizedBox(height: 8),
          Card(
            child: SwitchListTile(
              title: const Text('Modo escuro'),
              subtitle: const Text(
                'Tema escuro para melhor visualização',
                style: TextStyle(fontSize: 12, color: Color(0xFF808080)),
              ),
              secondary: Icon(
                isDark ? Icons.dark_mode : Icons.light_mode,
                color: colors.primary,
              ),
              value: isDark,
              onChanged: (value) {
                ref.read(darkModeProvider.notifier).state = value;
                ref.read(settingsRepositoryProvider).setDarkMode(value);
              },
            ),
          ),

          const SizedBox(height: 24),

          // Playlist
          _SectionTitle(text: 'Playlist', color: colors.primary),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  TextField(
                    controller: _urlController,
                    decoration: const InputDecoration(
                      labelText: 'URL da Playlist M3U',
                      hintText: 'https://...',
                      prefixIcon: Icon(Icons.link),
                    ),
                    maxLines: 2,
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      FilledButton.icon(
                        onPressed: _saveUrl,
                        icon: const Icon(Icons.save),
                        label: const Text('Salvar'),
                      ),
                      const SizedBox(width: 8),
                      OutlinedButton.icon(
                        onPressed: _resetUrl,
                        icon: const Icon(Icons.restore),
                        label: const Text('Restaurar padrão'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 24),

          // Data
          _SectionTitle(text: 'Dados', color: colors.primary),
          const SizedBox(height: 8),
          Card(
            child: Column(
              children: [
                ListTile(
                  leading: Icon(Icons.refresh, color: colors.onSurfaceVariant),
                  title: const Text('Atualizar playlist'),
                  subtitle: const Text(
                    'Baixar novamente a lista de canais',
                    style: TextStyle(fontSize: 12, color: Color(0xFF808080)),
                  ),
                  onTap: () {
                    ref.read(playlistProvider.notifier).refresh();
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                          content: Text('Atualizando playlist...')),
                    );
                  },
                ),
                const Divider(height: 1, indent: 16, endIndent: 16),
                ListTile(
                  leading: Icon(Icons.delete_outline,
                      color: colors.onSurfaceVariant),
                  title: const Text('Limpar histórico'),
                  subtitle: const Text(
                    'Remover canais assistidos recentemente',
                    style: TextStyle(fontSize: 12, color: Color(0xFF808080)),
                  ),
                  onTap: () async {
                    await ref
                        .read(historyRepositoryProvider)
                        .clearHistory();
                    if (!context.mounted) return;
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Histórico limpo')),
                    );
                  },
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // About
          _SectionTitle(text: 'Sobre', color: colors.primary),
          const SizedBox(height: 8),
          Card(
            child: ListTile(
              leading: Icon(Icons.info_outline, color: colors.primary),
              title: const Text('IPTV Player v1.0.0'),
              subtitle: const Text(
                'Player IPTV gratuito e open-source',
                style: TextStyle(fontSize: 12, color: Color(0xFF808080)),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _saveUrl() {
    final url = _urlController.text.trim();
    if (url.isNotEmpty) {
      ref.read(playlistUrlProvider.notifier).state = url;
      ref.read(settingsRepositoryProvider).setPlaylistUrl(url);
      ref.read(playlistProvider.notifier).refresh();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('URL salva. Atualizando playlist...')),
      );
    }
  }

  void _resetUrl() {
    _urlController.text = AppConstants.defaultPlaylistUrl;
    _saveUrl();
  }
}

class _SectionTitle extends StatelessWidget {
  final String text;
  final Color color;

  const _SectionTitle({required this.text, required this.color});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: TextStyle(
        color: color,
        fontWeight: FontWeight.w700,
        fontSize: 13,
        letterSpacing: 0.5,
      ),
    );
  }
}
