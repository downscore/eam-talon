{user.website} open: user.website_open_url(website)
{user.search_engine} hunt <user.prose>$: user.website_search_with_search_engine(search_engine, user.prose)
{user.search_engine} (that|this):
  text = user.selected_text()
  user.website_search_with_search_engine(search_engine, text)
{user.hostname}: user.switcher_focus_browser_tab_by_hostname(hostname)
