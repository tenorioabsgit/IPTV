' ContentTaskLogic.brs - Async playlist loading
' Based on SceneGraph Master Sample pattern

sub RunContentTask()
    m.contentTask = CreateObject("roSGNode", "PlaylistLoaderTask")
    m.contentTask.ObserveField("content", "OnMainContentLoaded")
    m.contentTask.control = "run"
    m.loadingIndicator.visible = true
end sub

sub OnMainContentLoaded()
    m.loadingIndicator.visible = false
    m.allContent = m.contentTask.content

    if m.allContent = invalid then return

    ' Build flat channel list for CH+/CH-
    m.allChannels = CreateObject("roArray", 0, true)
    if m.allContent.GetChildCount() > 0
        allCat = m.allContent.GetChild(0)
        for i = 0 to allCat.GetChildCount() - 1
            m.allChannels.Push(allCat.GetChild(i))
        end for
    end if

    ' Set content on GridScreen
    m.gridScreen.content = m.allContent
end sub
