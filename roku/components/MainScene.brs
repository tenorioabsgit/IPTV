sub Init()
    m.loadingIndicator = m.top.FindNode("loadingIndicator")

    ' State
    m.allContent = invalid
    m.allChannels = CreateObject("roArray", 0, true)
    m.currentChannelIndex = -1
    m.selectedChannel = invalid

    ' Initialize screen stack (from ScreenStackLogic.brs)
    InitScreenStack()

    ' Create and show GridScreen as root
    m.gridScreen = CreateObject("roSGNode", "GridScreen")
    m.gridScreen.visible = false
    ShowScreen(m.gridScreen)

    ' Setup GridScreen observers (from GridScreenLogic.brs)
    InitGridScreenLogic()

    ' Start loading playlist (from ContentTaskLogic.brs)
    RunContentTask()
end sub

function OnKeyEvent(key as String, press as Boolean) as Boolean
    if not press then return false

    currentScreen = GetCurrentScreen()

    ' Back button navigation
    if key = "back"
        if GetScreenStackSize() > 1
            CloseScreen(currentScreen)
            return true
        end if
        return false
    end if

    ' CH+/CH- in VideoScreen
    if currentScreen <> invalid
        nodeType = currentScreen.subtype()
        if nodeType = "VideoScreen"
            if key = "up" or key = "channelUp" or key = "fastforward"
                PlayNextChannel()
                return true
            else if key = "down" or key = "channelDown" or key = "rewind"
                PlayPreviousChannel()
                return true
            end if
        end if
    end if

    return false
end function
