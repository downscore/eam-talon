{user.website} open: user.open_url(website)
{user.search_engine} hunt <user.prose>$: user.search_with_search_engine(search_engine, user.prose)
{user.search_engine} (that|this):
  text = user.selected_text()
  user.search_with_search_engine(search_engine, text)
