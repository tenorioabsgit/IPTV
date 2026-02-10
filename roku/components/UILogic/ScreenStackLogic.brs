' ScreenStackLogic.brs - Navigation stack management
' Based on SceneGraph Master Sample pattern

sub InitScreenStack()
    m.screenStack = []
end sub

sub ShowScreen(node as Object)
    ' Hide previous screen
    prev = m.screenStack.Peek()
    if prev <> invalid
        prev.visible = false
    end if

    ' Add new screen to scene and stack
    m.top.AppendChild(node)
    node.visible = true
    node.SetFocus(true)
    m.screenStack.Push(node)
end sub

sub CloseScreen(node as Object)
    if m.screenStack.Count() = 0 then return

    ' Pop and remove current screen
    last = m.screenStack.Pop()
    last.visible = false
    m.top.RemoveChild(last)

    ' Restore previous screen
    prev = m.screenStack.Peek()
    if prev <> invalid
        prev.visible = true
        prev.SetFocus(true)
    end if
end sub

function GetCurrentScreen() as Object
    return m.screenStack.Peek()
end function

function GetScreenStackSize() as Integer
    return m.screenStack.Count()
end function
