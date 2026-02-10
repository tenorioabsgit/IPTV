' VideoPlayerLogic.brs - Video playback flow
' Based on SceneGraph Master Sample pattern

sub ShowVideoScreen(channelNode as Object)
    m.videoScreen = CreateObject("roSGNode", "VideoScreen")
    m.videoScreen.ObserveField("state", "OnVideoScreenStateChange")
    ShowScreen(m.videoScreen)
    m.videoScreen.callFunc("PlayVideo", channelNode)
end sub

sub OnVideoScreenStateChange()
    ' Handle video errors or completion at scene level if needed
end sub

sub PlayNextChannel()
    if m.allChannels.Count() = 0 then return
    m.currentChannelIndex = m.currentChannelIndex + 1
    if m.currentChannelIndex >= m.allChannels.Count()
        m.currentChannelIndex = 0
    end if
    m.videoScreen.callFunc("PlayVideo", m.allChannels[m.currentChannelIndex])
end sub

sub PlayPreviousChannel()
    if m.allChannels.Count() = 0 then return
    m.currentChannelIndex = m.currentChannelIndex - 1
    if m.currentChannelIndex < 0
        m.currentChannelIndex = m.allChannels.Count() - 1
    end if
    m.videoScreen.callFunc("PlayVideo", m.allChannels[m.currentChannelIndex])
end sub
