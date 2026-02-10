function IntToStr(num as Integer) as String
    s = Str(num)
    if Left(s, 1) = " " then s = Mid(s, 2)
    return s
end function

function TrimStr(s as String) as String
    while Len(s) > 0
        if Left(s, 1) = " " then s = Mid(s, 2) else exit while
    end while
    while Len(s) > 0
        if Right(s, 1) = " " then s = Left(s, Len(s) - 1) else exit while
    end while
    return s
end function

function RemoveCR(s as String) as String
    while Len(s) > 0
        if Right(s, 1) = Chr(13) then s = Left(s, Len(s) - 1) else exit while
    end while
    while Len(s) > 0
        if Left(s, 1) = Chr(13) then s = Mid(s, 2) else exit while
    end while
    return s
end function

function SplitLines(text as String) as Object
    result = CreateObject("roArray", 0, true)
    startPos = 1
    textLen = Len(text)
    while startPos <= textLen
        lfPos = Instr(startPos, text, Chr(10))
        if lfPos = 0
            segment = Mid(text, startPos)
            segment = RemoveCR(segment)
            result.Push(segment)
            startPos = textLen + 1
        else
            if lfPos > startPos
                segment = Mid(text, startPos, lfPos - startPos)
                segment = RemoveCR(segment)
                result.Push(segment)
            else
                result.Push("")
            end if
            startPos = lfPos + 1
        end if
    end while
    return result
end function

function GetAttrValue(txtLine as String, attrName as String) as String
    q = Chr(34)
    search = attrName + "=" + q
    foundPos = Instr(1, LCase(txtLine), LCase(search))
    if foundPos > 0
        valStart = foundPos + Len(search)
        valEnd = Instr(valStart, txtLine, q)
        if valEnd > valStart
            return Mid(txtLine, valStart, valEnd - valStart)
        end if
    end if
    return ""
end function

function GetStreamFormat(videoUrl as String) as String
    lower = LCase(videoUrl)
    if Instr(1, lower, ".m3u8") > 0 then return "hls"
    if Instr(1, lower, ".mpd") > 0 then return "dash"
    if Instr(1, lower, ".mp4") > 0 then return "mp4"
    if Instr(1, lower, ".mkv") > 0 then return "mkv"
    return "hls"
end function

function CleanCategoryTitle(categoryTitle as String) as String
    if categoryTitle = invalid or categoryTitle = "" then return ""
    parenPos = 0
    for c = 1 to Len(categoryTitle)
        if Mid(categoryTitle, c, 1) = "("
            parenPos = c
            exit for
        end if
    end for
    if parenPos > 1
        return TrimStr(Left(categoryTitle, parenPos - 2))
    end if
    return categoryTitle
end function

sub SortByName(arr as Object)
    n = arr.Count()
    if n < 2 then return
    for i = 0 to n - 2
        for j = 0 to n - 2 - i
            if arr[j].name > arr[j + 1].name
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
            end if
        end for
    end for
end sub

function FindNodeByUrl(content as Object, url as String) as Object
    for each row in content.GetChildren(-1, 0)
        for each item in row.GetChildren(-1, 0)
            if item.url = url then return item
        end for
    end for
    return invalid
end function
