sub Init()
    m.video = m.top.FindNode("video")
    m.osdGroup = m.top.FindNode("osdGroup")
    m.osdHints = m.top.FindNode("osdHints")
    m.osdChannelName = m.top.FindNode("osdChannelName")
    m.osdCategory = m.top.FindNode("osdCategory")
    m.bufferingGroup = m.top.FindNode("bufferingGroup")
    m.errorGroup = m.top.FindNode("errorGroup")
    m.errorMessage = m.top.FindNode("errorMessage")

    m.currentContent = invalid
    m.hasError = false

    ' Reusable OSD timer
    m.osdTimer = CreateObject("roSGNode", "Timer")
    m.osdTimer.duration = 3
    m.osdTimer.repeat = false
    m.osdTimer.ObserveField("fire", "HideOsd")

    ' Observe video state
    m.video.ObserveField("state", "OnVideoStateChange")
    m.video.ObserveField("bufferingStatus", "OnBufferingChange")
end sub

sub PlayVideo(channelNode as Object)
    m.currentContent = channelNode
    m.hasError = false
    m.errorGroup.visible = false
    m.bufferingGroup.visible = true

    ' Update OSD
    m.osdChannelName.text = channelNode.title
    if channelNode.description <> invalid and channelNode.description <> ""
        m.osdCategory.text = channelNode.description
    else
        m.osdCategory.text = ""
    end if

    ' Build video content
    videoContent = CreateObject("roSGNode", "ContentNode")
    videoContent.title = channelNode.title
    videoContent.url = channelNode.url
    if channelNode.streamFormat <> invalid and channelNode.streamFormat <> ""
        videoContent.streamFormat = channelNode.streamFormat
    else
        videoContent.streamFormat = "hls"
    end if

    m.video.content = videoContent
    m.video.control = "play"

    ShowOsd()
end sub

sub StopVideo()
    m.video.control = "stop"
end sub

sub OnVideoStateChange()
    state = m.video.state
    m.top.state = state

    if state = "playing"
        m.bufferingGroup.visible = false
        m.errorGroup.visible = false
        m.hasError = false
    else if state = "buffering"
        m.bufferingGroup.visible = true
    else if state = "error"
        m.hasError = true
        m.bufferingGroup.visible = false
        m.errorGroup.visible = true
        m.errorMessage.text = "Canal indisponivel no momento"
    else if state = "finished"
        ' Try to reconnect
        if m.currentContent <> invalid
            m.video.control = "play"
        end if
    end if
end sub

sub OnBufferingChange()
    status = m.video.bufferingStatus
    if status <> invalid
        if status.percentage < 100
            m.bufferingGroup.visible = true
        else
            m.bufferingGroup.visible = false
        end if
    end if
end sub

sub ShowOsd()
    m.osdGroup.visible = true
    m.osdHints.visible = true
    m.osdTimer.control = "stop"
    m.osdTimer.control = "start"
end sub

sub HideOsd()
    m.osdGroup.visible = false
    m.osdHints.visible = false
end sub

function OnKeyEvent(key as String, press as Boolean) as Boolean
    if not press then return false

    if key = "back"
        StopVideo()
        return false ' Let parent handle screen close
    end if

    if key = "OK"
        if m.hasError and m.currentContent <> invalid
            PlayVideo(m.currentContent)
            return true
        end if
        ' Toggle play/pause
        if m.video.state = "playing"
            m.video.control = "pause"
            ShowOsd()
        else if m.video.state = "paused"
            m.video.control = "resume"
            ShowOsd()
        end if
        return true
    end if

    if key = "play"
        if m.video.state = "playing"
            m.video.control = "pause"
        else if m.video.state = "paused"
            m.video.control = "resume"
        end if
        ShowOsd()
        return true
    end if

    ShowOsd()
    return false
end function
