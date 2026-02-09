sub init()
    m.rowList = m.top.findNode("rowList")
    m.videoPlayer = m.top.findNode("videoPlayer")
    m.loadingGroup = m.top.findNode("loadingGroup")
    m.heroGroup = m.top.findNode("heroGroup")
    m.heroPoster = m.top.findNode("heroPoster")
    m.heroChannelName = m.top.findNode("heroChannelName")
    m.heroCategory = m.top.findNode("heroCategory")
    m.channelCount = m.top.findNode("channelCount")

    ' State
    m.allContent = invalid
    m.isPlayerVisible = false

    ' All channels list for CH+/CH- navigation
    m.allChannels = createObject("roArray", 0, true)
    m.currentChannelIndex = -1

    ' Start loading playlist
    m.playlistTask = createObject("roSGNode", "PlaylistTask")
    m.playlistTask.observeField("output", "onPlaylistLoaded")
    m.playlistTask.control = "run"

    ' Observe RowList events
    m.rowList.observeField("rowItemFocused", "onRowItemFocused")
    m.rowList.observeField("rowItemSelected", "onRowItemSelected")

    ' Observe video player close
    m.videoPlayer.observeField("playerClosed", "onPlayerClosed")
end sub

sub onPlaylistLoaded()
    content = m.playlistTask.output
    if content = invalid then return

    m.allContent = content
    m.loadingGroup.visible = false
    m.heroGroup.visible = true
    m.rowList.visible = true

    ' Build flat channel list for CH+/CH-
    m.allChannels = createObject("roArray", 0, true)
    if content.getChildCount() > 0
        allCat = content.getChild(0)
        for i = 0 to allCat.getChildCount() - 1
            m.allChannels.push(allCat.getChild(i))
        end for
    end if

    ' Set channel count
    totalChannels = m.allChannels.count()
    countStr = str(totalChannels)
    if left(countStr, 1) = " " then countStr = mid(countStr, 2)
    m.channelCount.text = countStr

    ' Set content directly to RowList
    m.rowList.content = content

    ' Update hero with first channel
    if content.getChildCount() > 0 and content.getChild(0).getChildCount() > 0
        updateHero(content.getChild(0).getChild(0), content.getChild(0).title)
    end if

    m.rowList.setFocus(true)
end sub

sub onRowItemFocused()
    focused = m.rowList.rowItemFocused
    if focused = invalid then return

    rowIndex = focused[0]
    itemIndex = focused[1]

    if m.allContent = invalid then return
    if rowIndex < 0 or rowIndex >= m.allContent.getChildCount() then return

    row = m.allContent.getChild(rowIndex)
    if itemIndex < 0 or itemIndex >= row.getChildCount() then return

    updateHero(row.getChild(itemIndex), row.title)
end sub

sub updateHero(channelNode as object, categoryTitle as string)
    m.heroChannelName.text = channelNode.title

    ' Show category (strip the count suffix for cleaner display)
    if categoryTitle <> invalid and categoryTitle <> ""
        ' Remove " (N)" suffix from category name
        parenPos = 0
        for c = 1 to len(categoryTitle)
            if mid(categoryTitle, c, 1) = "("
                parenPos = c
                exit for
            end if
        end for
        if parenPos > 1
            cleanTitle = left(categoryTitle, parenPos - 2)
        else
            cleanTitle = categoryTitle
        end if
        m.heroCategory.text = cleanTitle
    else
        m.heroCategory.text = ""
    end if

    ' Update hero poster
    if channelNode.hdPosterUrl <> invalid and channelNode.hdPosterUrl <> ""
        m.heroPoster.uri = channelNode.hdPosterUrl
    else
        m.heroPoster.uri = ""
    end if
end sub

sub onRowItemSelected()
    selected = m.rowList.rowItemSelected
    if selected = invalid then return

    rowIndex = selected[0]
    itemIndex = selected[1]

    if m.allContent = invalid then return
    if rowIndex < 0 or rowIndex >= m.allContent.getChildCount() then return

    row = m.allContent.getChild(rowIndex)
    if itemIndex < 0 or itemIndex >= row.getChildCount() then return

    channelNode = row.getChild(itemIndex)

    ' Find index in all channels list for CH+/CH-
    for i = 0 to m.allChannels.count() - 1
        if m.allChannels[i].url = channelNode.url
            m.currentChannelIndex = i
            exit for
        end if
    end for

    playChannel(channelNode)
end sub

sub playChannel(channelNode as object)
    m.isPlayerVisible = true
    m.videoPlayer.visible = true
    m.heroGroup.visible = false
    m.rowList.visible = false

    m.videoPlayer.callFunc("playVideo", channelNode)
    m.videoPlayer.setFocus(true)
end sub

sub onPlayerClosed()
    m.isPlayerVisible = false
    m.videoPlayer.visible = false
    m.heroGroup.visible = true
    m.rowList.visible = true

    m.rowList.setFocus(true)
end sub

sub playNextChannel()
    if m.allChannels.count() = 0 then return
    m.currentChannelIndex = m.currentChannelIndex + 1
    if m.currentChannelIndex >= m.allChannels.count()
        m.currentChannelIndex = 0
    end if
    playChannel(m.allChannels[m.currentChannelIndex])
end sub

sub playPreviousChannel()
    if m.allChannels.count() = 0 then return
    m.currentChannelIndex = m.currentChannelIndex - 1
    if m.currentChannelIndex < 0
        m.currentChannelIndex = m.allChannels.count() - 1
    end if
    playChannel(m.allChannels[m.currentChannelIndex])
end sub

function onKeyEvent(key as string, press as boolean) as boolean
    if not press then return false

    if m.isPlayerVisible
        ' Player visible - handle channel switching
        ' Support multiple keys: up/channelUp/fastforward for next,
        ' down/channelDown/rewind for previous (CH+/CH- may not exist
        ' on all remotes or may be intercepted by Roku TV system)
        if key = "up" or key = "channelUp" or key = "fastforward"
            playNextChannel()
            return true
        else if key = "down" or key = "channelDown" or key = "rewind"
            playPreviousChannel()
            return true
        end if
        return false
    end if

    return false
end function
