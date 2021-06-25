<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.loc.gov/standards/alto/ns-v4#"
    xmlns:a="http://www.loc.gov/standards/alto/ns-v4#"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:template match="node()|comment()|@*">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()|comment()"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="a:TextLine">
        <xsl:choose>
            <xsl:when test="key('IDREF', @TAGREFS)/@LABEL = 'MusicLine'"/>
            <xsl:when test="key('IDREF', @TAGREFS)/@LABEL = 'DropCapitalLine'"/>
            <xsl:otherwise>
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()|comment()"/>
                </xsl:copy>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="a:TextBlock">
        <xsl:choose>
            <xsl:when test="key('IDREF', @TAGREFS)/@LABEL = 'MusicLine'"/>
            <xsl:otherwise>
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()|comment()"/>
                </xsl:copy>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:key name="IDREF" match="a:OtherTag" use="@ID"/>
    
</xsl:stylesheet>