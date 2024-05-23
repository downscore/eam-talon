{user.website} open: user.website_open_url(website)
{user.search_engine} hunt <user.prose>$: user.website_search_with_search_engine(search_engine, user.prose)
{user.search_engine} (that|this):
  text = user.selected_text_or_word()
  user.website_search_with_search_engine(search_engine, text)
{user.hostname}: user.cross_browser_focus_tab_by_hostname(hostname)
