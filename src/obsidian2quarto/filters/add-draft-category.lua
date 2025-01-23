function Meta(meta)
  print("Running filter...")
  if meta.draft == true then
    if not meta.categories then
      meta.categories = {}
    end
    if type(meta.categories) == "table" then
      table.insert(meta.categories, "draft")
    end
  end
  return meta
end 
