-- 有料の範囲を、公開するサイトとPDFから外す。
-- 冒頭の設定に paywall: true がある記事だけが対象（casebook/ と landscape/ の _metadata.yml で指定）。
--
-- どこから有料にするか
--   1. 見出しに {.paid} を付けた節があれば、そこから
--   2. 冒頭の設定に paywall-sections: 2 のような数があれば、その数の節までが無料
--   3. 冒頭の設定に paywall-free: 0.34 のような割合があれば、節の数にその割合を掛けた数（切り上げ）までが無料
--   4. 「（仮）」で始まる見出しの節から（ユースケースの記事の「（仮）自社の業務に入れるなら」）
--   5. どれもなければ、本文の節の後半から
-- 「関連する記事」「出典」「要確認」は、有料の範囲のあとに残す。
-- 文言は _variables.yml ではなく、この下の3行で変える。

local LEAD = "ここから先は有料です。"
local NOTE = "noteでも購入できます。"
local BUTTON = "サイトに有料登録する"
local TAIL = { ["関連する記事"] = true, ["出典"] = true, ["要確認"] = true, ["Sources"] = true, ["To be verified"] = true }

function Pandoc(doc)
  local flag = doc.meta.paywall
  if not flag or pandoc.utils.stringify(flag) ~= "true" then return doc end

  local heads = {}   -- 本文の節（末尾の3つを除く）の位置
  local tail_at = nil
  for i, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 2 then
      local text = pandoc.utils.stringify(b)
      if TAIL[text] then
        if not tail_at then tail_at = i end
      elseif not tail_at then
        table.insert(heads, { at = i, text = text, paid = b.classes:includes("paid") })
      end
    end
  end
  if #heads < 2 then return doc end

  local start = nil
  for n, h in ipairs(heads) do
    if h.paid then start = n break end
  end
  local fixed = doc.meta["paywall-sections"] and tonumber(pandoc.utils.stringify(doc.meta["paywall-sections"]))
  local ratio = doc.meta["paywall-free"] and tonumber(pandoc.utils.stringify(doc.meta["paywall-free"]))
  if not start and fixed then start = fixed + 1 end
  if not start and ratio then start = math.ceil(#heads * ratio) + 1 end
  if start and start > #heads then return doc end
  if not start then
    for n, h in ipairs(heads) do
      if h.text:sub(1, #"（仮）") == "（仮）" then start = n break end
    end
  end
  if not start then start = math.floor(#heads / 2) + 1 end
  if start < 2 then start = 2 end
  if start > #heads then return doc end

  local lead, note, button, list_title = LEAD, NOTE, BUTTON, "この先に書いてあること"
  if doc.meta.lang and pandoc.utils.stringify(doc.meta.lang) == "en" then
    lead, note, button, list_title = "The rest of this page is for paid members.", "", "Become a paid member", "What follows"
  end
  local out = {}
  for i = 1, heads[start].at - 1 do table.insert(out, doc.blocks[i]) end

  local items = {}
  for n = start, #heads do table.insert(items, { pandoc.Plain({ pandoc.Str(heads[n].text) }) }) end
  local box = {
    pandoc.Para({ pandoc.Strong({ pandoc.Str(lead) }) }),
    pandoc.Para({ pandoc.Str(list_title) }),
    pandoc.BulletList(items),
  }
  if quarto.doc.is_format("html") then
    table.insert(box, pandoc.RawBlock("html",
      '<p class="s2d-paywall-cta"><a class="s2d-button" data-s2d-register="paywall" href="/register.html">' .. button ..
      '</a><span class="s2d-paywall-note">' .. note .. '</span></p>'))
  else
    table.insert(box, pandoc.Para({ pandoc.Str("有料登録の案内は、サイトの「有料登録」のページにあります。" .. note) }))
  end
  table.insert(out, pandoc.Div(box, pandoc.Attr("", { "s2d-paywall" })))

  if tail_at then
    for i = tail_at, #doc.blocks do table.insert(out, doc.blocks[i]) end
  end
  doc.blocks = out
  return doc
end
