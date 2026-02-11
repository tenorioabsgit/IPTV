' ContentTaskLogic - from SceneGraph Master Sample

sub RunContentTask()
    m.contentTask = CreateObject("roSGNode", "PlaylistLoaderTask")
    m.contentTask.ObserveField("content", "OnMainContentLoaded")
    m.contentTask.control = "run"
    m.loadingIndicator.visible = true
end sub

sub OnMainContentLoaded()
    m.loadingIndicator.visible = false
    m.GridScreen.content = m.contentTask.content
    m.GridScreen.SetFocus(true)
end sub
