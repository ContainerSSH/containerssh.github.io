def declare_variables(variables, macro):
    @macro
    def since(version):
        "Add a button"
        HTML = """<a href="https://github.com/containerssh/containerssh/releases" target="_blank"><span class="since"><span class="since__hide">(</span><span class="since__text">since</span> <span class="since__value">%s</span><span class="since__hide">)</span></span></a>"""
        return HTML % (version)
    
    @macro
    def upcoming(version):
        "Upcoming version"
        HTML = """<span class="since"><span class="since__hide">(</span><span class="since__text">upcoming in</span> <span class="since__value">%s</span><span class="since__hide">)</span></span>"""
        return HTML % (version)