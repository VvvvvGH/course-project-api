from sqlalchemy import func, or_
from app.models.base_models import BidNotice, CorrectedNotice, PurchaseNotice
from app import db


class ProjectOngoing(PurchaseNotice, db.Model):
    def to_json(self):
        json_data = {
            "ProjID": self.ProjID,
            "ProjTitle": self.ProjTitle,
            "City": self.City,
            "ProjBud": self.ProjBud,
            "PurQuantity": self.PurQuantity,
            "ProjReqURL": self.ProjReqURL,
            "SupplierQuals": self.SupplierQuals,
            "DDL": self.DDL,
            "Addr": self.Addr,
            "BidStartTime": self.BidStartTime,
            "BidStartAddr": self.BidStartAddr,
            "BidBond": self.BidBond,
            "AnnounceDDL": self.AnnunceDDL,
            "Publisher": self.Publisher,
            "PubDate": self.PubDate,
            "Attachment": self.Attachment,
        }
        return json_data


class ProjectCorrected(CorrectedNotice, db.Model):
    def to_json(self):
        json_data = {
            "ProjID": self.ProjID,
            "Content": self.Content,
        }
        return json_data


class ProjectEnded(BidNotice, db.Model):
    def to_json(self):
        json_data = {
            "ProjID": self.ProjID,
            "ProjTitle": self.ProjTitle,
            "ProjBud": self.ProjBud,
            "PurMethod": self.PurMethod,
            "SBs": self.SBs,
            "QuoteDetail": self.QuoteDetail,
            "ServiceReq": self.ServiceReq,
            "Quantity": self.Quantity,
            "Currency": self.Currency,
            "UnitPrice": self.UnitPrice,
            "FinalPrice": self.FinalPrice,
            "ReviewDate": self.ReviewDate,
            "ReviewAddr": self.ReviewAddr,
            "ReviewCommittee": self.ReviewCommittee,
            "Manager": self.Manager,
            "ReviewComment": self.ReviewCommittee,
            "AnnounceDDL": self.AnnounceDDL,
            "Attachment": self.Attachment,
        }
        return json_data


class CityStatics(object):

    @staticmethod
    def count_all():
        ongoing_count = db.session.query(func.count(PurchaseNotice.ProjID)).first()[0]
        ended_count = db.session.query(func.count(BidNotice.ProjID)).first()[0]
        corrected_count = db.session.query(func.count(CorrectedNotice.ProjID)).first()[0]
        return ongoing_count, corrected_count, ended_count, ongoing_count + ended_count + corrected_count

    @staticmethod
    def count_cities():
        cities = []
        city_list = ['GD', 'GZ', 'SZ', 'ZH', 'ST', 'SG', 'FS', 'JM', 'ZJ', 'MM', 'HZ', 'MZ', 'SW', 'HY', 'YZ', 'QY',
                     'DG', 'ZS', 'JY', 'YF', 'SD']
        for city in city_list:
            ongoing_count = \
                db.session.query(func.count(PurchaseNotice.City)).filter(PurchaseNotice.City == city).first()[0]
            ended_count = db.session.query(func.count(BidNotice.City)).filter(BidNotice.City == city).first()[0]
            corrected_count = \
                db.session.query(func.count(CorrectedNotice.City)).filter(CorrectedNotice.City == city).first()[0]

            total_count = ongoing_count + ended_count + corrected_count
            if total_count:
                city_data = {
                    "City": city,
                    "TotalNumber": total_count,
                    "procurement_notices": ongoing_count,
                    "correction_notice": corrected_count,
                    "bid_notice": ended_count,
                }
                cities.append(city_data)

        return cities

    def to_json(self):
        count_all = self.count_all()
        json_data = {
            "ProjectStatistics": {
                "TotalNumber": count_all[3],
                "procurement_notices": count_all[0],
                "correction_notice": count_all[1],
                "bid_notice": count_all[2],
            },
            "Cities": self.count_cities()
        }
        return json_data


class ProjectList(object):
    def __init__(self, current_page, items_per_page, project_type, city, search_token):
        self.current_page = current_page
        self.items_per_page = items_per_page
        self.project_type = int(project_type)
        self.city = city
        self.search_token = search_token
        self.switch = {
            0: PurchaseNotice,
            1: ProjectCorrected,
            2: ProjectEnded,
        }

    def get_project_count(self):

        return db.session.query(func.count(self.switch[self.project_type].ProjID)).first()[0]

    def get_project_ids(self):

        # 根据发布时间排序
        # 根据城市过滤
        sql_query = self.switch[self.project_type].query
        if self.city:
            sql_query = sql_query.filter_by(City=self.city)
        if self.search_token:
            sql_query = sql_query.filter(
                or_(ProjectOngoing.ProjTitle.like("%%%s%%" % self.search_token),
                    ProjectOngoing.ProjID.like("%%%s%%" % self.search_token)))

        return sql_query

    def get_project_info(self, project_id):
        return self.switch[self.project_type].query.filter_by(ProjID=str(project_id)).first_or_404()

    def to_json(self):
        data = {
            "Page": {
                "PageCount": self.get_project_count() // self.items_per_page or 1,
                "CurrentPage": self.current_page,
                "ItemsPerPage": self.items_per_page,
            },
            "Project": []
        }
        types = ["采购公告", "更正公告", "结果公告"]
        project_ids = self.get_project_ids().order_by(self.switch[self.project_type].ReleaseDate).paginate(
            self.current_page,
            per_page=self.items_per_page,
            error_out=False
        ).items

        for item in project_ids:
            project = self.get_project_info(item.ProjID)
            project_info = {}
            if self.project_type == 0:
                project_info = {
                    "ProjID": project.ProjID,
                    "ProjTitle": project.ProjTitle,
                    "City": project.City,
                    "PubDate": project.PubDate,
                    "DDL": project.PubDate,
                    "Type": types[self.project_type],
                }
            elif self.project_type == 1:
                project_info = {
                    "ProjID": project.ProjID,
                    "City": project.City,
                    "Type": types[self.project_type],
                }

            elif self.project_type == 2:
                project_info = {
                    "ProjID": project.ProjID,
                    "ProjTitle": project.ProjTitle,
                    "City": project.City,
                    "Type": types[self.project_type],
                }
            data['Project'].append(project_info)
        return data
