' VideoPlayerLogic - from SceneGraph Master Sample
' Uses built-in Video node directly (no custom VideoScreen)

sub ShowVideoScreen(rowContent as Object, selectedItem as Integer)
    m.videoPlayer = CreateObject("roSGNode", "Video")
    m.selectedIndex[1] = selectedItem

    if selectedItem <> 0
        numOfChildren = rowContent.GetChildCount()
        children = rowContent.GetChildren(numOfChildren - selectedItem, selectedItem)
        rowNode = CreateObject("roSGNode", "ContentNode")
        for each child in children
            rowNode.AppendChild(child.Clone(false))
        end for
        m.videoPlayer.content = rowNode
    else
        m.videoPlayer.content = rowContent.Clone(true)
    end if

    m.videoPlayer.contentIsPlaylist = true
    ShowScreen(m.videoPlayer)
    m.videoPlayer.control = "play"
    m.videoPlayer.ObserveField("state", "OnVideoPlayerStateChange")
    m.videoPlayer.ObserveField("visible", "OnVideoVisibleChange")
end sub

sub OnVideoPlayerStateChange()
    state = m.videoPlayer.state
    if state = "error" or state = "finished"
        CloseScreen(m.videoPlayer)
    end if
end sub

sub OnVideoVisibleChange()
    if m.videoPlayer.visible = false and m.top.visible = true
        currentIndex = m.videoPlayer.contentIndex
        m.videoPlayer.control = "stop"
        m.videoPlayer.content = invalid
        screen = GetCurrentScreen()
        screen.SetFocus(true)
        if screen.HasField("jumpToItem")
            screen.jumpToItem = currentIndex + m.selectedIndex[1]
        else if screen.HasField("jumpToRowItem")
            m.GridScreen.jumpToRowItem = [m.selectedIndex[0], currentIndex + m.selectedIndex[1]]
        end if
    end if
end sub
