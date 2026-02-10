import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit_video/media_kit_video.dart';
import '../../../core/constants/app_constants.dart';
import '../../../data/models/channel.dart';
import '../../../providers/player_provider.dart';
import '../../../providers/playlist_provider.dart';
import '../../../providers/search_provider.dart';
import '../../../providers/settings_provider.dart';
import '../../widgets/category_sidebar.dart';
import '../../widgets/channel_card.dart';
import '../../widgets/mini_player.dart';
import '../player/player_screen.dart';
import '../favorites/favorites_screen.dart';
import '../settings/settings_screen.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  late final VideoController _videoController;
  final _searchController = TextEditingController();
  final FocusNode _rootFocusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    final player = ref.read(playerProvider.notifier).player;
    _videoController = VideoController(player);
  }

  @override
  void dispose() {
    _searchController.dispose();
    _rootFocusNode.dispose();
    super.dispose();
  }

  KeyEventResult _handleKeyEvent(FocusNode node, KeyEvent event) {
    if (event is! KeyDownEvent) return KeyEventResult.ignored;

    final key = event.logicalKey;
    final channels = ref.read(filteredChannelsProvider);
    final notifier = ref.read(playerProvider.notifier);
    final hasChannel = ref.read(playerProvider).currentChannel != null;

    if (hasChannel && key == LogicalKeyboardKey.channelUp) {
      notifier.playNextChannel(channels);
      return KeyEventResult.handled;
    }
    if (hasChannel && key == LogicalKeyboardKey.channelDown) {
      notifier.playPreviousChannel(channels);
      return KeyEventResult.handled;
    }

    if (hasChannel &&
        (key == LogicalKeyboardKey.mediaPlayPause ||
            key == LogicalKeyboardKey.mediaPlay ||
            key == LogicalKeyboardKey.mediaPause)) {
      notifier.togglePlayPause();
      return KeyEventResult.handled;
    }

    return KeyEventResult.ignored;
  }

  bool get _isDesktop =>
      MediaQuery.of(context).size.width >= AppConstants.desktopBreakpoint;

  void _openFullScreen() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => PlayerScreen(videoController: _videoController),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final playerState = ref.watch(playerProvider);
    final hasActiveChannel = playerState.currentChannel != null;

    if (_isDesktop) {
      return _buildDesktopLayout(hasActiveChannel);
    }
    return _buildMobileLayout(hasActiveChannel);
  }

  Widget _buildDesktopLayout(bool hasActiveChannel) {
    const overscan = EdgeInsets.all(27.0);

    return Focus(
      focusNode: _rootFocusNode,
      onKeyEvent: _handleKeyEvent,
      child: Scaffold(
        body: Padding(
          padding: Platform.isAndroid ? overscan : EdgeInsets.zero,
          child: FocusTraversalGroup(
            policy: ReadingOrderTraversalPolicy(),
            child: Row(
              children: [
                // Sidebar
                Container(
                  width: 240,
                  color: const Color(0xFF111111),
                  child: Column(
                    children: [
                      _buildSidebarHeader(),
                      const Expanded(child: CategorySidebar()),
                    ],
                  ),
                ),
                // Subtle divider
                Container(width: 1, color: const Color(0xFF1E1E1E)),
                // Channel list (main focus area)
                Expanded(
                  flex: 3,
                  child: Column(
                    children: [
                      ExcludeFocus(child: _buildTopBar()),
                      Expanded(child: _buildChannelContent()),
                    ],
                  ),
                ),
                // Player panel
                if (hasActiveChannel) ...[
                  Container(width: 1, color: const Color(0xFF1E1E1E)),
                  SizedBox(
                    width: 420,
                    child: _buildPlayerPanel(),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMobileLayout(bool hasActiveChannel) {
    return Focus(
      onKeyEvent: _handleKeyEvent,
      child: Scaffold(
        appBar: AppBar(
          title: Row(
            children: [
              Text(
                'IPTV',
                style: TextStyle(
                  color: Theme.of(context).colorScheme.primary,
                  fontWeight: FontWeight.w800,
                  fontSize: 18,
                ),
              ),
              const SizedBox(width: 4),
              const Text(
                'Player',
                style: TextStyle(
                  color: Color(0xFF555555),
                  fontWeight: FontWeight.w400,
                  fontSize: 16,
                ),
              ),
            ],
          ),
          actions: [
            IconButton(
              icon: const Icon(Icons.favorite),
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(
                    builder: (_) =>
                        FavoritesScreen(videoController: _videoController)),
              ),
            ),
            IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              ),
            ),
          ],
        ),
        drawer: Drawer(
          backgroundColor: const Color(0xFF111111),
          child: SafeArea(
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Icon(Icons.live_tv,
                          color: Theme.of(context).colorScheme.primary,
                          size: 20),
                      const SizedBox(width: 8),
                      Text(
                        'Categorias',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: Theme.of(context).colorScheme.onSurface,
                        ),
                      ),
                    ],
                  ),
                ),
                const Divider(height: 1),
                const Expanded(child: CategorySidebar()),
              ],
            ),
          ),
        ),
        body: Column(
          children: [
            _buildSearchBar(),
            Expanded(child: _buildChannelContent()),
            if (hasActiveChannel)
              MiniPlayer(
                videoController: _videoController,
                onExpand: _openFullScreen,
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildSidebarHeader() {
    final colors = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 16, 16, 12),
      decoration: const BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Color(0xFF1E1E1E), width: 1),
        ),
      ),
      child: Row(
        children: [
          Icon(Icons.live_tv, color: colors.primary, size: 22),
          const SizedBox(width: 8),
          Text(
            'IPTV',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w800,
              color: colors.primary,
            ),
          ),
          const SizedBox(width: 4),
          const Text(
            'Player',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w400,
              color: Color(0xFF555555),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar() {
    final colors = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: const BoxDecoration(
        color: Color(0xFF0D0D0D),
        border: Border(
          bottom: BorderSide(color: Color(0xFF1E1E1E), width: 1),
        ),
      ),
      child: Row(
        children: [
          Expanded(child: _buildSearchBar()),
          const SizedBox(width: 8),
          _buildViewToggle(),
          IconButton(
            icon: Icon(Icons.refresh, color: colors.onSurfaceVariant, size: 20),
            tooltip: 'Atualizar playlist',
            onPressed: () => ref.read(playlistProvider.notifier).refresh(),
          ),
          if (_isDesktop) ...[
            IconButton(
              icon: Icon(Icons.favorite, color: colors.onSurfaceVariant, size: 20),
              tooltip: 'Favoritos',
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(
                    builder: (_) =>
                        FavoritesScreen(videoController: _videoController)),
              ),
            ),
            IconButton(
              icon: Icon(Icons.settings, color: colors.onSurfaceVariant, size: 20),
              tooltip: 'Configurações',
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return SizedBox(
      height: 40,
      child: TextField(
        controller: _searchController,
        decoration: InputDecoration(
          hintText: 'Buscar canais...',
          prefixIcon: const Icon(Icons.search, size: 18),
          suffixIcon: _searchController.text.isNotEmpty
              ? IconButton(
                  icon: const Icon(Icons.clear, size: 18),
                  onPressed: () {
                    _searchController.clear();
                    ref.read(searchQueryProvider.notifier).state = '';
                  },
                )
              : null,
          isDense: true,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: BorderSide.none,
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: BorderSide(
              color: Theme.of(context).colorScheme.primary,
              width: 1,
            ),
          ),
          filled: true,
          fillColor: const Color(0xFF1A1A1A),
          contentPadding: const EdgeInsets.symmetric(vertical: 0),
        ),
        onChanged: (value) =>
            ref.read(searchQueryProvider.notifier).state = value,
      ),
    );
  }

  Widget _buildViewToggle() {
    final isGrid = ref.watch(gridViewProvider);
    return IconButton(
      icon: Icon(
        isGrid ? Icons.view_list : Icons.grid_view,
        color: Theme.of(context).colorScheme.onSurfaceVariant,
        size: 20,
      ),
      tooltip: isGrid ? 'Modo lista' : 'Modo grade',
      onPressed: () {
        ref.read(gridViewProvider.notifier).state = !isGrid;
        ref.read(settingsRepositoryProvider).setGridView(!isGrid);
      },
    );
  }

  Widget _buildChannelContent() {
    final channels = ref.watch(filteredChannelsProvider);
    final isGrid = ref.watch(gridViewProvider);
    final playlistState = ref.watch(playlistProvider);

    return playlistState.when(
      loading: () => const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(strokeWidth: 2),
            SizedBox(height: 16),
            Text(
              'Carregando playlist...',
              style: TextStyle(color: Color(0xFF555555)),
            ),
          ],
        ),
      ),
      error: (e, _) => Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline,
                size: 48, color: Color(0xFF555555)),
            const SizedBox(height: 16),
            Text(
              'Erro ao carregar: $e',
              style: const TextStyle(color: Color(0xFF808080)),
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: () => ref.read(playlistProvider.notifier).refresh(),
              icon: const Icon(Icons.refresh),
              label: const Text('Tentar novamente'),
            ),
          ],
        ),
      ),
      data: (_) {
        if (channels.isEmpty) {
          return const Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.search_off, size: 48, color: Color(0xFF444444)),
                SizedBox(height: 16),
                Text(
                  'Nenhum canal encontrado',
                  style: TextStyle(color: Color(0xFF808080)),
                ),
              ],
            ),
          );
        }

        if (isGrid) {
          return _buildGrid(channels);
        }
        return _buildList(channels);
      },
    );
  }

  Widget _buildGrid(List<Channel> channels) {
    final crossAxisCount = _isDesktop ? 4 : 3;
    return GridView.builder(
      padding: const EdgeInsets.all(12),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        childAspectRatio: 1.35,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
      itemCount: channels.length,
      itemBuilder: (_, i) => ChannelCard(channel: channels[i]),
    );
  }

  Widget _buildList(List<Channel> channels) {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      itemCount: channels.length,
      itemBuilder: (_, i) => ChannelListTile(channel: channels[i]),
    );
  }

  Widget _buildPlayerPanel() {
    final playerState = ref.watch(playerProvider);
    final channel = playerState.currentChannel;
    final colors = Theme.of(context).colorScheme;

    return Container(
      color: const Color(0xFF111111),
      child: Column(
        children: [
          // Video (tap to fullscreen)
          GestureDetector(
            onTap: _openFullScreen,
            child: AspectRatio(
              aspectRatio: 16 / 9,
              child: ExcludeFocus(
                child: Video(
                  controller: _videoController,
                  controls: (state) => const SizedBox.shrink(),
                ),
              ),
            ),
          ),
          // Accent line below video
          Container(
            height: 2,
            color: colors.primary.withValues(alpha: 0.4),
          ),
          // Channel info + actions
          if (channel != null)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    channel.name,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFFEEEEEE),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Container(
                        width: 6,
                        height: 6,
                        decoration: const BoxDecoration(
                          color: Color(0xFFFF3333),
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 6),
                      Text(
                        channel.group,
                        style: const TextStyle(
                          color: Color(0xFF808080),
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      FilledButton.tonalIcon(
                        autofocus: true,
                        onPressed: _openFullScreen,
                        icon: const Icon(Icons.fullscreen),
                        label: const Text('Tela cheia'),
                      ),
                      const SizedBox(width: 8),
                      IconButton(
                        icon: const Icon(Icons.stop,
                            color: Color(0xFF808080)),
                        onPressed: () =>
                            ref.read(playerProvider.notifier).stop(),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          // Status
          if (playerState.isBuffering)
            const Padding(
              padding: EdgeInsets.all(16),
              child: Row(
                children: [
                  SizedBox(
                    width: 14,
                    height: 14,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                  SizedBox(width: 8),
                  Text(
                    'Carregando...',
                    style: TextStyle(
                      color: Color(0xFF555555),
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          if (playerState.error != null)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Icon(Icons.error, color: colors.error, size: 14),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      playerState.error!,
                      style: TextStyle(color: colors.error, fontSize: 11),
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
