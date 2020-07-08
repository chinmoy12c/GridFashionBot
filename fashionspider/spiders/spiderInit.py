class SpiderInit:

    def __init__(self):
        self.siteRules = {
            'https://www.vogue.co.uk/fashion/fashion-trends' : {
                "siteId" : "Vouge",
                "sectionHead" : 'h3::text',
                "followLink" : '[data-test-id="Anchor"]::attr(href)',
                "sectionImageRule" : '[data-test-id="PictureWrapper"] [data-test-id="Img"]::attr(srcset)',
                "relativeTo" : 'https://www.vogue.co.uk',
                "subsectionHead" : '[data-test-id="GalleryImage"] h2::text',
                "isSrcSet" : True,
                "hasSectionImage" : True,
                "subsectionImgRule" : '[data-test-id="PictureWrapper"] img::attr(srcset)',
                "imgRelativeTo" : ''
            },

            'https://patternbank.com/trends' : {
                "siteId" : "PatternBank",
                "sectionHead" : 'h3::text',
                "followLink" : 'div.widgetSection__content a.widgetSectionLink::attr(href)',
                "sectionImageRule" : 'div.imageContainer img::attr(srcset)',
                "relativeTo" : '',
                "subsectionHead" : 'div.widgetSection__content div.titleRow h3::text',
                "isSrcSet" : True,
                "hasSectionImage" : True,
                "subsectionImgRule" : 'div.imageContainer div img::attr(srcset)',
                "imgRelativeTo" : ''
            },

            'https://www.collezioni.info/en/shows/page/3/' : {
                "siteId" : "Collezioni",
                "sectionHead" : '[id="moveTop"] h2::text',
                "followLink" : 'ul.pagination a::attr(href)',
                "sectionImageRule" : "none",
                "relativeTo" : '',
                "subsectionHead" : 'div.sectionsDetSingle h2::text',
                "isSrcSet" : False,
                "hasSectionImage" : False,
                "subsectionImgRule" : 'div.sectionsDetSingle a img::attr(src)',
                "imgRelativeTo" : 'https://www.collezioni.info'
            },

            #Celeb section sites
            "https://www.vogue.in/fashion/fashion-trends" : {
                "siteId" : "Celebrity Section",
                "sectionHead" : 'h3::text',
                "followLink" : '[data-test-id="Anchor"]::attr(href)',
                "sectionImageRule" : '[data-test-id="PictureWrapper"] [data-test-id="Img"]::attr(srcset)',
                "relativeTo" : 'https://www.vogue.in/',
                "subsectionHead" : '[data-test-id="GalleryImage"] h2::text',
                "isSrcSet" : False,
                "hasSectionImage" : True,
                "subsectionImgRule" : 'div.InstagramWrapper-sc-1d9wlcl-2 blockquote::attr(data-instgrm-permalink)',
                "imgRelativeTo" : '',
                "imgTail" : '/media?size=l'
            } 
        }
