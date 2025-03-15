import json

from fastapi import APIRouter
from fastapi_restful.cbv import cbv
from starlette.responses import StreamingResponse

from service.search_engine import GoogleSearchEngine
from service.translator import EmojiTranslator

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)


@cbv(router)
class SearchEndpoint:
    engine = GoogleSearchEngine()
    translator = EmojiTranslator()

    @router.get("/{query}", openapi_extra={})
    async def search(self, query: str):
        """
        {'title': 'string', 'snippet': 'string', 'image': 'string(optional)'}
        """
        text_query = await self.translator.translate_text(query)
        print(query + " -> " + text_query)
        responses = await self.engine.search(text_query)
        
        print(json.dumps(responses, indent=4, ensure_ascii=False))

        async def generate():
            for item in responses:
                item_title = await self.translator.translate_emoji(
                    content_type="title", text=item["title"]
                )
                item_snippet = await self.translator.translate_emoji(
                    content_type="snippet", text=item["snippet"]
                )
                data = {"title": item_title, "snippet": item_snippet}
                if item.get("pagemap"):
                    if item["pagemap"].get("metatags"):
                        for meta_tag in item["pagemap"]["metatags"]:
                            if "og:image" in meta_tag:
                                data["image"] = meta_tag["og:image"]
                                
                if item.get('link'):
                    data['link'] = item['link']
                    
                print(json.dumps(data, indent=4, ensure_ascii=False))
                    
                yield json.dumps(data) + "\n"

        return StreamingResponse(generate(), media_type="application/json")
